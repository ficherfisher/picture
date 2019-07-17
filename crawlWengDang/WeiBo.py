import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re
import pdfkit
header = {
    'Cookie':'SSOLoginState=1563361324;M_WEIBOCN_PARAMS=uicode%3D20000174;SUB=_2A25wK3B8DeRhGeBH7FAR9SfFyziIHXVT1BA0rDV6PUJbktANLWfCkW1NQaJVb4AiW217Wx1n9voDAAIvj9yT28Wn;MLOGIN=1;SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5YBI6XW1rvV.ivMzaw5x7A5JpX5KzhUgL.Foq4S0z7SK.4ehB2dJLoIEXLxK.LBo.L12qLxKBLBo.L12zLxK-L12BL1KMLxK.LBonLBKeLxKnL1h5L1h-t;SUHB=0A05EKA8B_CuE6;WEIBOCN_FROM=1110006030;_T_WM=50514472084;XSRF-TOKEN=78b8d2',    #cookie
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'

}
params = {
    "hideSearchFrame":"",
    "keyword":"北京风景",#可自行设置搜索关键词
    "page":1#可自行设置爬取页数
}
Content = []
def Anaylsis(div):
    information = {}
    information['name'] = ""#用户名
    information['content'] = ""#微博内容
    information['img'] = ""#图片信息
    information['upvote'] = ""#点赞数量
    information['time'] = ""#时间
    if len(div.find_all(attrs={"class":"nk"})) == 0:
        return
    else:
        try:#解析所需信息
            information['name'] = div.find(attrs={"class": "nk"}).get_text()#使用get_text()函数时，要求为单元格及只能使用find()不能使用fine_all()
            information['content'] = div.find(attrs={"class": "ctt"}).get_text()
            information['time'] = div.find(attrs={"class": "ct"}).get_text()
            As = str(div.find_all('a')).split(",")
            for a in As:
                if re.search(r"组图共", a) and information['img'] == "":
                    information['img'] = "1\t" + a.split("\"")[1]
                if re.search(r"原图", a) and information['img'] == "":
                    information['img'] = "2\t" + a.split("\"")[1]
                #解析图片url，并设置标志位
                if re.search(r"赞", a):
                    information['upvote'] = a.split(">")[1].split("<")[0]
            Content.append(information)
        except:
            print("解析错误")
def SavePicture(img,name):
    count = 1
    if img.split("\t")[0] == "1":
        test = requests.get(img.split("\t")[1],headers = header)
        soup = BeautifulSoup(test.text,"lxml")
        divs = soup.find_all(attrs={"class":"c"})
        for div in divs:
            As = str(div.find_all('a')).split(",")
            for a in As:
                if re.search(r"原图",a):
                    with open("D:/python/crawl/crawlWengDang/WeiBo/{}.jpg".format(name+str(count)), "wb") as f:
                        f.write(requests.get("https://weibo.cn" + a.split("\"")[1].replace("amp;",""),headers = header).content)
                    print(name+str(count) + "保存成功")
                    count = count + 1
    """
    if img.split("\t")[0] == "2":
        with open("D:/ython/crawl/crawlWengDang/WeiBo/{}.jpg".format(name), "wb") as f:
            f.write(requests.get(img.split("\t")[1]).content)
    """
    return count
    #根据不同标志位，用不同方式保存图片
def Save():
    String = ""
    for content in Content:
        name = content['name']
        tempContent = content['content']
        img = content['img']
        upvote = content['upvote']
        time = content['time']
        #将待保存信息集合H5保存到pdf中
        if img != "":
            count = SavePicture(img,name)
            String = String + "<h3>" + name + "</h3><p>" + tempContent + "</p><p>共有" +str(count) + "张图片</p><p>" + upvote + time + "</p>"
        else:
            String = String + "<h3>" + name + "</h3><p>" + tempContent + "</p><p>没有图片</p><p>" + upvote + time + "</p>"

    options = {
        'page-size': 'A4',
        'margin-top': '10',
        'margin-right': '10',
        'margin-bottom': '5',
        'margin-left': '10',
        'encoding': 'UTF-8',
        'outline-depth': 1000,
    }#设置pdf中的位置，字体格式等信息
    file = 'D:/python/crawl/crawlWengDang/WeiBo/{}.pdf'.format("北京风景")
    config = pdfkit.configuration(wkhtmltopdf=r'D:\software\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(String, file, options=options, configuration=config)
    pass
def Main():
    NewUrl = "https://weibo.cn/search/mblog?" + urlencode(params)#根据搜索关键词生成url，
    test = requests.get(NewUrl, headers=header)
    soup = BeautifulSoup(test.text, "html.parser")
    divs = soup.find_all(attrs={"class": "c"})
    for div in divs:
        Anaylsis(div)
    Save()
if __name__ == "__main__":
    Main()