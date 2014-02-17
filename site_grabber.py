__author__ = 'dimas'

from xml_write import XmlWriter
from grab import Grab
import re


BASE_URL = 'https://barrick.taleo.net/'

SEARCH_URL = 'https://barrick.taleo.net/careersection/2/jobsearch.ftl'

job_url = 'https://barrick.taleo.net/careersection/jobdetail.ftl?job={0}'


def barrick_grabber(params=None, url=None):
    if not url:
        url = SEARCH_URL
    if not params:
        params = '&keyword=managers'

    xml_writer = XmlWriter(scraper_name='barrick')
    g = Grab()
    g.setup(headers={'Cache-Control': 'private', 'P3P': 'CP="CAO PSA OUR', 'Transfer-Encoding': 'chunked'})
    g.setup(post=params)
    g.go(url)
    html = g.response.body
    jobs = re.findall(r'job=([^(]*)%', html)
    jobs = jobs[len(jobs) / 2:]
    for job in jobs:
        xml_writer.append_job(url_data=job_url.format(job), key_data=job)

    xml_writer.write_doc()