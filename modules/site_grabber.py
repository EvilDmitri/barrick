#!/usr/bin/python
# -*- coding: utf-8 -*-
import HTMLParser

import datetime
import logging
import urllib

__author__ = 'dimas'

import re

from grab import Grab, GrabTimeoutError

from modules.xml_write import XmlWriter
from modules.settings import *


j = \
    ['073248', '073247', '073244', '073228', '073235', '073237', '072827', '072826', '073225', '073226', '072829', '073204', '073147', '073207', '073205', '073072', '073197', '073162', '073169', '073193', '073168', '073164', '073108', '073157', '072364']


def get_data_from_html(data):
    """Cleans data from tags, special symbols"""
    snippet = urllib.unquote(data)
    h = HTMLParser.HTMLParser()
    snippet = h.unescape(snippet)
    s = snippet[3:]
    snippet = s.encode('utf-8')

    TAG_RE = re.compile(r'<[^>]+>')
    snippet = TAG_RE.sub('', snippet)

    pClnUp = re.compile(r'\n|\t|\xa0|0xc2|\\')
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
                      snippet_data=snippet, date_added_data=datetime.datetime.now().strftime('%Y%m%d%I%m'), company_data=company
                      )

    return True


def barrick_grabber(url=None, params=None, file_name=None, company=None):
    if url is None:
        url = SEARCH_URL
    else:
        url = url + SEARCH

    if company is None:
        company = 'barrick'

    if params is None:
        params = '&keyword='
    params += '&dropListSize=200'

    if file_name is None:
        data_parsed = datetime.datetime.now()
        file_name = company + '-' + data_parsed.strftime('%Y%m%d%I%m%S') + '.xml'

    xml_writer = XmlWriter(scraper_name=file_name)

    g = Grab()
    # g.setup(headers={
    #     'Cache-Control': 'private',
    #     'P3P': 'CP="CAO PSA OUR',
    #     'Transfer-Encoding': 'chunked',
    # })
    g.setup(post=params)
    try:
        g.go(url)

    except GrabTimeoutError:
        logging.error(u'error|timeout|%s' % GrabTimeoutError)
        logging.critical(u'error|Service unavailable')
        return

    html = g.response.body
    # ToDo Find ALL the Jobs (data.html)
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