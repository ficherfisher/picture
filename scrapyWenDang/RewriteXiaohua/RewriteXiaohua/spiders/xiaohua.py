# -*- coding: utf-8 -*-
import scrapy
from RewriteXiaohua.items import RewritexiaohuaItem


class XiaohuaSpider(scrapy.Spider):
    name = 'xiaohua'
    allowed_domains = ['xiaohuar.com']
    start_urls = []
    for num in range(1,20):
        url = "http://www.xiaohuar.com/list-1-"+str(num)+".html"
        start_urls.append(url)

    def parse(self, response):
        item = RewritexiaohuaItem()
        itemTs = response.xpath('//div[@class="item_t"]')
        for itemT in itemTs:
            item['img'] = itemT.xpath('//div[@class="img"]/a/img/@src').extract()
            item['title'] = itemT.xpath('//span/a/text()').extract()
        return item
