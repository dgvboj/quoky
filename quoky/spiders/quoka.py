# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
import datetime
import sys


# TODO: use a library for this
# Converts a country prefix to a country name
COUNTRIES = {
    'D': 'Deutschland',
    'NL': 'Nederlands',
    'A': u'Östereich',
    'PL': 'Pollen',
}


def correct_prices(data, fields):
    '''5.000.000,- -> 5000000 '''
    for field in fields:
        value = data[field]
        if value:
            # Not possible to use "translate" here because of str/unicode issues
            value = value.replace('.', '').replace(',', '').replace('-', '')
            data[field] = int(value)
        else:
            data[field] = None


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
        try:
            # Now get the next page, rinse and repeat
            #  We use the "next page" link, which is easier to use than the direct page links
            next_url = response.css(
                ('body > div.spr-wrp > div.cnv > div.cnt > '
                 'main > div.page-navigation-bottom.rslt-pagination-container.style-facelift > '
                 'div > div > div > ul > li.arr-rgt.active > a')).xpath('@href').extract()[0]
            yield scrapy.Request(response.urljoin(next_url), self.city_pager)
        except:
            # No next page
            pass

    def parse_city(self, response):
        for url in response.xpath('//*[@id="ResultListData"]/ul/li').xpath('.//div[2]/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), self.parse_detail)

    def parse_detail(self, response):
        detail = response.css('body > div.spr-wrp > div.cnv > div.cnt > main > div.box.bdr-grey.docked.detail > div')
        FIELDS_CSS_PATHS = [
            ('OBID',             'div.data > div:nth-child(2) > div.date-and-clicks > strong:nth-child(2)'),
            ('country-code',     'div.data > div:nth-child(2) > div.location > strong > span > span > span.country-name.country'),
            ('Stadt',            'div.data > div:nth-child(2) > div.location > strong > span > a > span'),
            ('PLZ',              'div.location > strong > span > span > span.postal-code'),
            ('Ueberschrift',     'div.headline > h2'),
            ('Beschreibung',     'div.data > div:nth-child(3) > div'),
            ('Kaufpreis',        'div.price.has-type > strong > span'),
            ('Telefon',          'div.meta > div.box.bdr-grey.cust-links > div > ul > li > span > span'),
            ('cust-type',        'div.meta > div.box.bdr-grey.cust-links > div > div.cust-type'),
        ]
        data = {}
        for field, csspath in FIELDS_CSS_PATHS:
            try:
                data[field] = detail.css(csspath).xpath('text()').extract()[0].strip()
            except:
                data[field] = None
        data['Erstellungsdatum'] = ''.join(response.xpath('/html/body/div[3]/div[2]/div[1]/main/div[8]/div/div[3]/div[2]/div[2]/text()').extract()).strip()
        # I use a naive UTC datetime (no timezone)
        mytime = datetime.datetime.utcnow()
        data['erzeugt_am'] = mytime
        data['url'] = response.url
        # country-code is not needed, we need Land
        data['Land'] = COUNTRIES[data.pop('country-code')]
        # drop cust-type, set gewerblich
        cust_type = data.pop('cust-type')
        if cust_type == 'Gewerblicher Inserent':
            gewerblich = 1
        elif cust_type == 'Privater Inserent':
            gewerblich = 0
        else:
            gewerblich = -1
        data['Gewerblich'] = gewerblich
        parts = response.url.split('/')
        data['Boersen_ID'] = parts[6] if parts[3] == 'qpi' else parts[5]
        data['Immobilientyp'] = u'Büros, Gewerbeflächen'
        data['Vermarktungstyp'] = 'kaufen'
        data['Monat'] = mytime.month
        # Fill fields marked as empty in the requirements
        EMPTY_FIELDS = [
            'Anbieter_ObjektID', 'Immobilientyp_detail', 'Bundesland',
            'Bezirk', 'Strasse', 'Hausnummer', 'Etage', 'Kaltmiete',
            'Warmmiete', 'Nebenkosten', 'Zimmeranzahl', 'Wohnflaeche'
        ]
        for field in EMPTY_FIELDS:
            data[field] = None
        correct_prices(data, ['Kaufpreis', 'Kaltmiete', 'Warmmiete', 'Nebenkosten'])
        yield data
