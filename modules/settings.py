#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

FILE_PATH = os.path.realpath(__file__).split(os.path.sep)[-1]

BASE_URL = 'https://barrick.taleo.net/'
SEARCH = 'careersection/2/jobsearch.ftl'
SEARCH_URL = BASE_URL + SEARCH

job_url = 'https://barrick.taleo.net/careersection/jobdetail.ftl?job={0}'