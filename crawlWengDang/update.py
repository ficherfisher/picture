import requests
from bs4 import BeautifulSoup
import time
import random
import os
Dirpath = "C:/Users/peng/Pictures/Camera Roll/"
def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)
def Save(urls):
    count = 1
    for url in urls:
        try:
            with open(Dirpath + str(count) + ".jpg", "wb") as f:
                f.write(requests.get(url).content)
            print("save successfully " + str(count) + ".jpg")
        except:
            print("fail")
        count = count + 1
    return count
def getPictureUrl(startUrls):
    pictureUrls = []
    for url in startUrls:
        text = requests.get(url)
        text.encoding = "gbk"
        soup = BeautifulSoup(text.text,"lxml")
        div = soup.find(attrs={"class":"list"})
        Lis = div.find_all('li')
        count = 1
        for li in Lis:
            if count != 3:
                href = li.find('a').get('href')
                text1 = requests.get("http://www.netbian.com/" + href)
                text1.encoding = "gbk"
                soup = BeautifulSoup(text1.text,"lxml")
                div = soup.find(attrs={"class":"pic"})
                pictureUrls.append(div.find('img').get('src'))
                count = count + 1
            else:
                count = count + 1
    return pictureUrls
def Main():
    keyWord = ["dongman/","fengjing/","meinv/","youxi/","yingshi/",
               "weimei/","sheji/","keai/","huahui/","dongwu/",
               "jieri/","meishi/","shuiguo/","jianzhu/","feizhuliu/",
               "s/wangzherongyao/","s/huyan/"
               ]
    startUrls = []
    temp = keyWord[random.randint(0,16)]
    for number in range(1,4):
        if number == 1:
            startUrls.append("http://www.netbian.com/"+temp+"index" + ".htm")
        else:
            startUrls.append("http://www.netbian.com/"+temp+"index_"+str(number) + ".htm")

    print("total:"+ str(Save(getPictureUrl(startUrls)))+"theme:"+ temp)
    time.sleep(2)

if __name__ == "__main__":
    del_file(Dirpath)
    Main()
"""
动态更新桌面壁纸，获取高清

"""
