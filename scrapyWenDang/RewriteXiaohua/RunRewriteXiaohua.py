from scrapy import cmdline
import datetime
StartTime = datetime.datetime.now()
cmdline.execute("scrapy crawl xiaohua".split())
EndTime = datetime.datetime.now()
print(EndTime-StartTime)
