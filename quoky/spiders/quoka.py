# -*- coding: utf-8 -*-
import scrapy


class QuokySpider(scrapy.Spider):

    name = 'quokaspider'
    allowed_domains = ['www.quoka.de']
    start_urls = ['http://www.quoka.de/immobilien/bueros-gewerbeflaechen']

    def parse(self, response):
        pass
