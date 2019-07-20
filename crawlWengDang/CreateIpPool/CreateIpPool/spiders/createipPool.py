# -*- coding: utf-8 -*-
import scrapy


class CreateippoolSpider(scrapy.Spider):
    name = 'createipPool'
    allowed_domains = ['createipPool.com']
    start_urls = ['http://createipPool.com/']

    def parse(self, response):
        pass
