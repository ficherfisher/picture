import requests
from bs4 import BeautifulSoup
import os
import datetime
StartTime = datetime.datetime.now()
url = "http://m.xiaohuar.com/wap-1-2075.html"
test = requests.get(url)
test.encoding = "utf-8"
soup = BeautifulSoup(test.content,'html.parser')
temps = soup.find_all(attrs={"class":"swiper-slide"})
count = 0
for a in temps:
    pictureUrl = a.find('img').get('lazysrc')
    print(pictureUrl)
    base_dir = os.getcwd()
    count = count + 1
    with open(base_dir + "/xiaohua Data/" + str(count) + ".jpg","wb") as file:
        try:
            stream = requests.get(pictureUrl)
            file.write(stream.content)
            print(str(count) + ".jpg 保存成功")
        except:
            print("无法打开网址")

EndTime = datetime.datetime.now()
print(EndTime-StartTime)