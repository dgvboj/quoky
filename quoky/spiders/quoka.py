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
        # TODO: First, get the data in this page
        # Now get the next page, rinse and repeat
        #  We use the "next page" link, which is easier to use than the direct page links
        try:
            next_url = response.css(
                ('body > div.spr-wrp > div.cnv > div.cnt > '
                'main > div.page-navigation-bottom.rslt-pagination-container.style-facelift > '
                'div > div > div > ul > li.arr-rgt.active > a')).xpath('@href').extract()[0]
            yield scrapy.Request(response.urljoin(next_url), self.city_pager)
        except:
            # We have reached the last url, nothing more to do
            pass
