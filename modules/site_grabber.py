__author__ = 'dimas'

import re
import os

from grab import Grab, GrabTimeoutError

from modules.xml_write import XmlWriter


FILE_PATH = os.path.realpath(__file__).split(os.path.sep)[-1]

BASE_URL = 'https://barrick.taleo.net/'

SEARCH_URL = 'https://barrick.taleo.net/careersection/2/jobsearch.ftl'

job_url = 'https://barrick.taleo.net/careersection/jobdetail.ftl?job={0}'


def job_grabber(page, writer):
    url = job_url.format(page)
    g = Grab()
    g.go(url)
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

    writer.append_job(url_data=url, key_data=key, title_data=title, country_data=country, state_data=state, city_data=city,
                      date_posted_data=date_posted, provider_data='barrickscraper'
                      )


def barrick_grabber(params=None, url=None):
    if not url:
        url = SEARCH_URL
    if not params:
        params = '&keyword=managers'

    xml_writer = XmlWriter(scraper_name='barrick')

    g = Grab()
    g.setup(headers={'Cache-Control': 'private', 'P3P': 'CP="CAO PSA OUR', 'Transfer-Encoding': 'chunked'})
    g.setup(post=params)
    try:
        g.go(url)
    except GrabTimeoutError:
        print 'error|timeout'
        return

    html = g.response.body
    jobs = re.findall(r'job=([^(]*)%', html)
    if not jobs:
        print 'error|nojobs'
        return

    jobs = jobs[len(jobs) / 2:]
    for job in jobs:
        job_grabber(job, xml_writer)


    xml_writer.write_doc()