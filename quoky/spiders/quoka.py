# -*- coding: utf-8 -*-
import scrapy
import datetime


# TODO: use a library for this
COUNTRIES = {
    'D': 'Deutschland',
    'NL': 'Nederlands',
    'A': u'Östereich',
    'PL': 'Pollen',
}


class QuokySpider(scrapy.Spider):

    name = 'quokaspider'
    allowed_domains = ['www.quoka.de']
    start_urls = ['http://www.quoka.de/immobilien/bueros-gewerbeflaechen']

    def parse(self, response):
        for url in response.css('body > div.spr-wrp > div.cnv > div.cnt > aside > form > div:nth-child(5) > div > ul > li > ul > li > a').xpath('@href').extract():
            yield scrapy.Request(response.urljoin(url), self.city_pager)

    def city_pager(self, response):
        # First, get the data in this page
        for data in self.parse_city(response):
            yield data
        # Now get the next page, rinse and repeat
        #  We use the "next page" link, which is easier to use than the direct page links
        next_url = response.css(
            ('body > div.spr-wrp > div.cnv > div.cnt > '
             'main > div.page-navigation-bottom.rslt-pagination-container.style-facelift > '
             'div > div > div > ul > li.arr-rgt.active > a')).xpath('@href').extract()[0]
        yield scrapy.Request(response.urljoin(next_url), self.city_pager)

    def parse_city(self, response):
        for url in response.xpath('//*[@id="ResultListData"]/ul/li').xpath('//li/div[2]/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), self.parse_gewerblich)

    def parse_core(self, response, gewerblich):
        detail = response.css('body > div.spr-wrp > div.cnv > div.cnt > main > div.box.bdr-grey.docked.detail > div')
        FIELDS_CSS_PATHS = [
            ('OBID',             'div.data > div:nth-child(2) > div.date-and-clicks > strong:nth-child(2)'),
            ('country-code',     'div.data > div:nth-child(2) > div.location > strong > span > span > span.country-name.country'),
            ('Stadt',            'div.data > div:nth-child(2) > div.location > strong > span > a > span'),
            ('PLZ',              'div.location > strong > span > span > span.postal-code'),
            (u'Überschrift',     'div.headline > h2'),
            (u'Beschreibung',    'div.data > div:nth-child(3) > div'),
            ('Kaufpreis',        'div.price.has-type > strong > span'),
            ('Telefon',          'div.meta > div.box.bdr-grey.cust-links > div > ul > li > span > span'),
            ('Erstellungsdatum', 'div.data > div:nth-child(2) > div.date-and-clicks > span'),
        ]
        data = {}
        for field, csspath in FIELDS_CSS_PATHS:
            try:
                data[field] = detail.css(csspath).xpath('text()').extract()[0].strip()
            except:
                data[field] = None
        # I use a naive UTC datetime (no timezone)
        mytime = datetime.datetime.utcnow()
        data['erzeugt_am'] = mytime
        data['url'] = response.url
        # country-code is not needed, we need Land
        data['Land'] = COUNTRIES[data.pop('country-code')]
        data['Boersen_ID'] = 'xxx'
        data['Immobilientyp'] = 'Büros, Gewerbeflächen'
        data['Vermarktungstyp'] = 'kaufen'
        data['Monat'] = mytime.month
        data['Gewerblich'] = gewerblich
        # Fill fields marked as empty in the requirements
        EMPTY_FIELDS = [ 'Anbieter_ObjektID', 'Immobilientyp_detail', 'Bundesland', 'Bezirk', 'Strasse', 'Hausnummer', 'Etage', 'Kaltmiete', 'Warmmiete', 'Nebenkosten', 'Zimmeranzahl', 'Wohnflaeche' ]
        for field in EMPTY_FIELDS:
            data[field] = None
        yield data

    def parse_gewerblich(self, response):
        for data in self.parse_core(response, 1):
            yield data

    def parse_privat(self, response):
        for data in self.parse_core(response, 0):
            yield data
