import requests
from bs4 import BeautifulSoup
import pdfkit
import re
contentUrl = []
contentTitle = []
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Mobile Safari/537.36"
}#设置请求头信息
def analysis(soup):
    ul = soup.find_all(attrs={"class": "uk-nav uk-nav-side"})[1]
    As = ul.find_all(attrs={"class": "x-wiki-index-item"})
    for a in As:
        url = a.get("href")
        title = a.get_text("a")
        url = "https://www.liaoxuefeng.com" + url
        contentUrl.append(url)
        contentTitle.append(title)
#从网页源代码中解析出目录的url和目录的题目
def getContent(url):
    test = requests.get(url,headers=headers)
    soup = BeautifulSoup(test.text,"html.parser")
    div = soup.find(attrs={"class":"x-wiki-content x-main-content"})
    ps = str(div).split("\n")#将网页源代码按“\n”切割成字符数组
    newString = ""
    for p in ps:
        if re.search(r'data-src',p): #这里使用正则表达式的知识，作用是将带有图片的url解析出来并替换原来的字符串
            p = "<p color:red font-size:20px>https://www.liaoxuefeng.com" + p.split("\"")[3] + "</p>"
        newString = newString + p + "\n"
    return newString
#从网页源代码中解析出每个小标题的具体内容，并将带有图片的url解析出来
def save(Name):
    options = {
        'page-size': 'A4',
        'margin-top': '10',
        'margin-right': '10',
        'margin-bottom': '5',
        'margin-left': '10',
        'encoding': 'UTF-8',
        'outline-depth': 1000,
    }#设置pdf中的位置，字体格式等信息
    file = 'D:/liaoxuefeng/{}.pdf'.format(Name)
    config = pdfkit.configuration(wkhtmltopdf=r'D:\software\wkhtmltopdf\bin\wkhtmltopdf.exe')
    #这里是设置wkhtmltopdf.exe的执行路径，如果你已经将它加入到环境变量中，这里就不需要再设置
    Content = ""
    count = 0
    for url in contentUrl:
        information = getContent(url)
        Content = Content + information
        print(contentTitle[count] + "  保存成功")
        count = count + 1
        #获取全部url的全部内容，并保存到Content中
    pdfkit.from_string(Content, file, options=options, configuration=config)
    #调用pdfkit中的字符串函数写入pdf中
#保存成pdf
def Main():
    url = "https://www.liaoxuefeng.com/wiki/1252599548343744/1280507291631649"
    test = requests.get(url, headers=headers)
    soup = BeautifulSoup(test.text, "html.parser")
    analysis(soup)
    save(contentTitle[0])
#主函数
if __name__ == "__main__":
    Main()





