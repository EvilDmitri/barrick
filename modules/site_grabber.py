#!/usr/bin/python
# -*- coding: utf-8 -*-

import HTMLParser

import datetime
import logging
import urllib
import re

from grab import Grab, GrabTimeoutError

from modules.xml_write import XmlWriter
from modules.settings import *


TAG_RE = re.compile(r'<[^>]+>')
pClnUp = re.compile(r'\n|\t|\xa0|0xc2|\\')


def get_data_from_html(data):
    """Cleans data from tags, special symbols"""
    snippet = urllib.unquote(data)
    h = HTMLParser.HTMLParser()
    snippet = h.unescape(snippet)
    s = snippet[3:]
    snippet = s.encode('utf-8')
    # Clean from tags
    snippet = TAG_RE.sub('', snippet)
    #Clean from command chars
    clean_text = str(pClnUp.sub('', snippet))

    snippet = clean_text[:1000]
    return snippet.decode('utf8', 'ignore')


def job_grabber(page, writer, company):
    url = job_url.format(page)
    print '----------------'
    print 'Job URL - ', url
    g = Grab()
    try:
        g.go(url)
    except GrabTimeoutError:
        logging.error(u'error|timeout|%s' % GrabTimeoutError)
    data = g.doc.select('//input[@name="initialHistory"]')

    values = data.attr('value').split('!|!')

    snippet = get_data_from_html(values[19])

    key = values[16]
    title = values[15] + '-' + key

    location = values[22]
    locations = location.split('-')
    country = None
    state = None
    city = None
    try:
        country = locations[0]
        state = locations[1]
        city = locations[2]
    except IndexError:
        pass

    date_posted = ','.join(values[28].split(',')[:-1])

    writer.append_job(url_data=url, key_data=key, title_data=title, country_data=country, state_data=state,
                      city_data=city, date_posted_data=date_posted, provider_data=company + 'scraper',
                      snippet_data=snippet, date_added_data=datetime.datetime.now().strftime('%Y%m%d%I%m'),
                      company_data=company
                      )

    return True


def barrick_grabber(url=None, params=None, file_name=None, company=None, pages=None):
    if url is None:
        url = SEARCH_URL
    else:
        url = url + SEARCH

    if company is None:
        company = 'barrick'

    if params is None:
        params = '&keyword='

    if pages is None:
        params += '&dropListSize=25'
    else:
        params += '&dropListSize=%s' % str(25 * pages)

    if file_name is None:
        data_parsed = datetime.datetime.now()
        file_name = company + '-' + data_parsed.strftime('%Y%m%d%I%m%S') + '.xml'

    xml_writer = XmlWriter(scraper_name=file_name)

    g = Grab()
    g.setup(post=params)
    try:
        g.go(url)

    except GrabTimeoutError:
        logging.error(u'error|timeout|%s' % GrabTimeoutError)
        logging.critical(u'error|Service unavailable')
        return

    html = g.response.body
    jobs = re.findall(r'job=([^(]*)%', html)
    if not jobs:
        logging.error(u'error|nojobs')
        return

    jobs = jobs[len(jobs) / 2:]
    logging.info(u'Found %s jobs. Scraping...' % len(jobs))
    print '--------------------------------'
    print u'Found %s jobs. Scraping...' % len(jobs)
    success = 0
    for job in jobs:
        pass
        result = job_grabber(page=job, writer=xml_writer, company=company)
        if result:
            print u'Job nr.%s - scraped' % job
            success += 1

    logging.info(u'%s jobs scraped' % success)
    print u'%s jobs scraped' % success

    xml_writer.write_doc(file_name)