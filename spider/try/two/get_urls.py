import requests
from bs4 import BeautifulSoup
import pdfkit
import time


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
}

def urls():
    url = "https://www.liaoxuefeng.com"
    text = requests.get(url, headers=header)
    soup = BeautifulSoup(text.text, "lxml")
    marks = soup.find(attrs={"class": "uk-navbar-nav uk-hidden-small"})
    urls = marks.find_all('a')
    useful_urls = []

    for url in urls:
        temp = url.get('href')
        useful_urls.append(temp)
    useful_urls = list(filter(lambda id_str: '/wiki' in id_str, useful_urls))
    title = []
    mark = marks.get_text().split()
    counter_1 = 4
    while counter_1 <= 7:
        title.append(mark[counter_1])
        counter_1 = counter_1 + 1
    contents = []
    counter = 0
    for temp in title:
        information = {}
        information['title'] = temp
        information['url'] = "https://www.liaoxuefeng.com" + useful_urls[counter]
        counter = counter + 1
        contents.append(information)
    #print(contents)
    return contents

def more_urls(url):
    depict = []
    lead_urls = []
    titles = []
    text = requests.get(url,headers=header)
    soup = BeautifulSoup(text.text,'lxml')
    temps = soup.find(attrs={"id":"x-wiki-index"})
    temps_1 = temps.find_all('a')

    for url in temps_1:
        temp = url.get('href')
        temp_1 = url.get_text()
        lead_urls.append(temp)
        titles.append(temp_1)
    lead_urls = list(filter(lambda id_str:'/wiki' in id_str,lead_urls))
    counter = 0
    for title in titles:
        information = {}
        information['url'] = "https://www.liaoxuefeng.com" + lead_urls[counter]
        information['title'] = str(title)
        depict.append(information)
        counter = counter + 1
    return depict

#获取侧导航条的url，按顺序即可。
#新建函数获取一个教程全部url的信息，
#新建函数保存信息，以pdf格式
content = []
def contents(counter,title,url):
    time.sleep(10)
    text = requests.get(url,headers=header)
    soup = BeautifulSoup(text.text,'lxml')
    html = soup.find(attrs={"class":"x-wiki-content x-main-content"})
    string = "<h2>" + title + "</h2>"
    html_1 = string + str(html)
    content.append(html_1)
    print(title)
"""
    file = 'F:/爬虫/spider/try/three/{}.pdf'.format(1)
    path_wk = r'D:\python\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wk)
    pdfkit.from_string(html_1, file, options=options,configuration=config)
    print(title)
"""

def save_pdf(title,tttt):
    string = ""
    for s in tttt:
        string = string + str(s)
    options = {
        'page-size':'A4',
        'margin-top':'10',
        'margin-right':'10',
        'margin-bottom':'5',
        'margin-left':'10',
        'encoding':'UTF-8',
        'outline-depth':1000,
    }
    file = 'E:\pycharm\crawl/spider/try/three/{}.pdf'.format(str(title))
    path_wk = r'D:\software\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wk)
    pdfkit.from_string(string, file, options=options, configuration=config)


if __name__ == "__main__":
    time.sleep(5)
    first_urls = urls()
    for url in first_urls:
        sec = more_urls(first_urls[3]['url'])
        counter = 1
        for url_1 in sec:
            contents(counter, url_1['title'], url_1['url'])
            counter = counter + 1

        save_pdf(first_urls[3]['title'],content)
        content.clear()
