from selenium import webdriver
import requests
import os
Dirnum = 0
def VisitDir(path):
    global Dirnum   #global类型，定义Dirnum为全局变量
    for list in os.listdir(path):
        SubPath = os.path.join(path,list)
        if os.path.isdir(SubPath):
            Dirnum = Dirnum + 1
            VisitDir(SubPath)
    return Dirnum - 1
#使用递归函数，遍历path路径下的文件夹数量并返回
#作用：当终止程序后再次运行时，爬取相同的漫画会紧接上次爬取的某一话
def mkDir(path):
    if not os.path.exists(path):
        os.mkdir(path)
#检测文件夹是否存在
def savePicture(filename,url):
    with open(filename,'wb') as f:
        f.write(requests.get(url).content)
#保存图片
def getUrl(indexUrl):
    pictureUrl = []
    browser = webdriver.Chrome()
    browser.get(indexUrl)
    browser.implicitly_wait(3) #等待3秒
    title = browser.title.split(',')[0]  #获取漫画名
    mkDir(title)
    #找到该漫画每一集的url
    for comicList in browser.find_elements_by_class_name('comic_Serial_list'):
        Urls = comicList.find_elements_by_tag_name('a')
        for Url in Urls:
            pictureUrl.append(Url.get_attribute('href'))
        # 获得每集url
    browser.quit()
    Comics = dict(name = title,urls = pictureUrl)
    return Comics
#获取该漫画的名字和更新到当前集的所有url
def getPictureUrl(Comics):
    EpisodeUrls = Comics['urls']
    title = Comics['name']
    temp = VisitDir(title)
    NewEpisodeUrls = []
    while temp < len(EpisodeUrls):
        NewEpisodeUrls.append(EpisodeUrls[temp])
        temp = temp + 1
    #检测之前爬取该漫画的集数，筛选漫画每一集的url，紧接之前的工作继续爬取
    for url in NewEpisodeUrls:
        browser = webdriver.Chrome()
        browser.get(url)
        browser.implicitly_wait(5)
        mkDir(title+"/"+browser.title.split("-")[1])
        #获取漫画具体的哪一集，并创建文件夹
        pageNum = len(browser.find_elements_by_tag_name('option'))
        #获取漫画某一集具体的图片页数
        nextpage = browser.find_element_by_xpath('//*[@id="AD_j1"]/div/a[4]')
        #找到H5中的下一页，Javascript的语法
        for tempNum in range(pageNum):
            PictureUrl = browser.find_element_by_id('curPic').get_attribute('src')
            filename = title+"/"+browser.title.split("-")[1]+"/"+str(tempNum)+'.png'
            savePicture(filename,PictureUrl)
            nextpage.click()
        print("当前章节\t{}  下载完毕".format(browser.title))
        browser.quit()
#获取每一集中具体每一页漫画的url，并调用savePicture()函数保存
def Main():
    url = input("输入漫画首地址：")
    getPictureUrl(getUrl(url))
if __name__ == "__main__":
    Main()