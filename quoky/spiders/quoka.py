# -*- coding: utf-8 -*-
import scrapy


class QuokySpider(scrapy.Spider):

    name = 'quokaspider'
    allowed_domains = ['www.quoka.de']
    start_urls = ['http://www.quoka.de/immobilien/bueros-gewerbeflaechen']

    def parse(self, response):
        for url in response.css('body > div.spr-wrp > div.cnv > div.cnt > aside > form > div:nth-child(5) > div > ul > li > ul > li > a').xpath('@href').extract():
            yield scrapy.Request(response.urljoin(url), self.city_pager)

    def city_pager(self, response):
        pass
