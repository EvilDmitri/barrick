#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import etree


class XmlWriter():
    def __init__(self, scraper_name='', date='',
                 ):

        self.scraper_name = scraper_name
        self.data_parsed = date

        self.data = etree.Element('data',
                                  scraper='{0}'.format(scraper_name),
                                  date='{0}'.format(self.data_parsed)
                                  )

        self.doc = etree.ElementTree(self.data)

    def append_job(self,
                   key_data=None,
                   title_data=None,
                   company_data=None,
                   city_data=None,
                   state_data=None,
                   country_data=None,
                   url_data=None,
                   snippet_data=None,
                   date_posted_data=None,
                   date_added_data=None,
                   provider_data=None):

        job = etree.Element('job')
        self.data.append(job)

        key = etree.SubElement(job, 'key')
        if key_data:
            key.text = etree.CDATA(key_data)

        title = etree.SubElement(job, 'title')
        if title_data:
            title.text = etree.CDATA(title_data)

        company = etree.SubElement(job, 'company')
        if company_data:
            company.text = etree.CDATA(company_data)

        city = etree.SubElement(job, 'city')
        if city_data:
            city.text = etree.CDATA(city_data)

        state = etree.SubElement(job, 'state')
        if state_data:
            state.text = etree.CDATA(state_data)

        country = etree.SubElement(job, 'country')
        if country_data:
            country.text = etree.CDATA(country_data)

        url = etree.SubElement(job, 'url')
        if url_data:
            url.text = etree.CDATA(url_data)

        snippet = etree.SubElement(job, 'snippet')
        if snippet_data:
            snippet.text = etree.CDATA(snippet_data)

        date_posted = etree.SubElement(job, 'date_posted')
        if date_posted_data:
            date_posted.text = etree.CDATA(date_posted_data)

        date_added = etree.SubElement(job, 'date_added')
        if date_added_data:
            date_added.text = etree.CDATA(date_added_data)

        provider = etree.SubElement(job, 'provider')
        if provider_data:
            provider.text = etree.CDATA(provider_data)

    def write_doc(self, file_name):
        with open(file_name, 'w') as outFile:
            self.doc.write(outFile, xml_declaration=True, encoding='utf-16', pretty_print=True)