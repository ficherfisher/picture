# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import os

class RewritexiaohuaPipeline(object):
    def process_item(self, item, spider):
        baseDir = os.getcwd()
        count = 0
        for img in item['img']:
            title = item['title'][count]
            with open(baseDir+"/Data/"+title+".png","wb") as f:
                try:
                    f.write(requests.get("http://www.xiaohuar.com/"+str(img)).content)
                    print("success  " + title)
                except:
                    print("fail")
            count = count + 1
        return item
