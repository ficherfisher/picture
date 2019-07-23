# -*- coding: utf-8 -*-
import scrapy
from CreateIpPool.items import CreateippoolItem

class AgentSpider(scrapy.Spider):
    name = 'agent'
    allowed_domains = ['daili.com']
    start_urls = []
    for i in range(1,50):
        start_urls.append("https://www.xicidaili.com/nn/"+str(i))

    def parse(self, response):
        item = CreateippoolItem()
        Odds = response.xpath('//tr[@class="odd"]')
        for odd in Odds:
            ip = odd.xpath('td/text()').extract()[0]
            part = odd.xpath('td/text()').extract()[1]
            item['address'] = ip + ":" + part
            yield item
        pass
