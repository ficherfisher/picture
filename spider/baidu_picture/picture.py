from urllib.parse import urlencode
import requests
import re
import os
import random
import time
save_dir='C:/Users/peng/Pictures/Camera Roll/'  #定义全局变量
dirnum = 0
def visitdir(path):
    dirnum = len(os.listdir(path))
    return dirnum

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

def baidtu_uncomplie(url):
    res = ''
    c = ['_z2C$q', '_z&e3B', 'AzdH3F']
    d= {'w':'a', 'k':'b', 'v':'c', '1':'d', 'j':'e', 'u':'f', '2':'g', 'i':'h', 't':'i', '3':'j', 'h':'k', 's':'l', '4':'m', 'g':'n', '5':'o', 'r':'p', 'q':'q', '6':'r', 'f':'s', 'p':'t', '7':'u', 'e':'v', 'o':'w', '8':'1', 'd':'2', 'n':'3', '9':'4', 'c':'5', 'm':'6', '0':'7', 'b':'8', 'l':'9', 'a':'0', '_z2C$q':':', '_z&e3B':'.', 'AzdH3F':'/'}
    if(url==None or 'http' in url):
        return url
    else:
        j= url

        for m in c:
            j=j.replace(m,d[m])
        for char in j:
            if re.match('^[a-w\d]+$',char):
                char = d[char]
            res= res+char
        return res   #翻译图片网址
#从objurl到真实图片url转换


def get_page(offset,string):
    params = {
        'tn': 'resultjson_com',
        'ipn': 'rj',
        'ct':'201326592',
        'is':'',
        'fp': 'result',
        'queryWord': string,   #搜索的关键词
        'cl': '2',
        'lm': '-1',
        'ie': 'utf-8',         #网页的编码格式为utf-8
        'oe': 'utf-8',
        'adpicid':'',
        'st': '-1',
        'z':'',
        'ic': '0',
        'word': string,        #搜索的关键词
        's':'',
        'se':'',
        'tab':'',
        'width':'',
        'height':'',
        'face': '0',
        'istype': '2',
        'qc':'',
        'nc': '1',
        'fr':'',
        'expermode':'',
        'pn': offset*30,      #表示显示了多少装图片一般取值为offset*30   offset=n
        'rn': '30',
        'gsm': '1e',
        '1537355234668':'',
    }  #预定义，这是header里面的内容
    url = 'https://image.baidu.com/search/acjson?' + urlencode(params) #整合变换成标准url
    #根据header的信息，调用函数urlencode()整合成可以直接获取previow中的内容


    try:
        response = requests.get(url)   #获取当前url网页的信息保存到response
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)      #尝试着打开网站，如果网站为空，则不做以下操作
#只使用调用一次


def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            if item.get('fromPageTitle'):
                title = item.get('fromPageTitle')
            else:
                title='noTitle'
            image = baidtu_uncomplie(item.get('objURL'))
            if(image):
                yield { 'image': image,'title': title  }   #如果image为空则返回image，否则就返回title     ???????


def save_image(item,count):
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = save_dir+'{0}.{1}'.format(str(count), 'jpg')  #建立路径
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:  #文件指针f
                    f.write(response.content)
                    print('succuer:',count,'.jpg')
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')



#保存图片


def main(pageIndex,count,string):
    json = get_page(pageIndex,string)       #调用get_page函数，打开百度图片首页，获得网页信息 网页解析preview中的内容
    for image in get_images(json):
        save_image(image, count)
        count += 1
    return count
#主函数

if __name__=='__main__':
    del_file(save_dir)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    count=visitdir(save_dir)
    #生成文件夹
    string = "高清壁纸"
    keyword = ["动漫","唯美","风景","星空","美女","宇宙"]
    string = keyword[random.randint(0,5)] + string
    for i in range(1,2):
        count=main(i,count,string)  #循环抓取图片调用main函数

    print('total:',count,"thume:" ,string)
    time.sleep(2)

