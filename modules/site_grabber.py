#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import logging

__author__ = 'dimas'

import re

from grab import Grab, GrabTimeoutError

from modules.xml_write import XmlWriter
from settings import *


def job_grabber(page, writer, snippet):
    url = job_url.format(page)
    g = Grab()
    try:
        g.go(url)
    except GrabTimeoutError:
        logging.error(u'error|timeout|%s' % GrabTimeoutError)
    data = g.doc.select('//input[@name="initialHistory"]')

    values = data.attr('value').split('!|!')

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
                      city_data=city, date_posted_data=date_posted, provider_data='barrickscraper', snippet_data=snippet
                      )

    return True


def barrick_grabber(url=None, params=None, file_name=None):
    if not url:
        url = SEARCH_URL
    else:
        url = url + SEARCH

    if not params:
        params = '&keyword='

    if not file_name:
        data_parsed = datetime.datetime.now()
        file_name = 'barrick' + '-' + data_parsed.strftime('%Y%m%d%I%m%S') + '.xml'

    xml_writer = XmlWriter(scraper_name=file_name)

    g = Grab()
    g.setup(headers={'Cache-Control': 'private', 'P3P': 'CP="CAO PSA OUR', 'Transfer-Encoding': 'chunked'})
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
    print u'Found %s jobs. Scraping...' % len(jobs)

    success = 0
    for job in jobs:
        result = job_grabber(job, xml_writer, params)
        if result:
            success += 1
    logging.info(u'%s jobs scraped' % success)
    print u'%s jobs scraped' % success

    xml_writer.write_doc(file_name)