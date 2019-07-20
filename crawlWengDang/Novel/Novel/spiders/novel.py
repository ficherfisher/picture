# -*- coding: utf-8 -*-
import scrapy


class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = ['novel.com']
    start_urls = ['http://novel.com/']

    def parse(self, response):
        pass
