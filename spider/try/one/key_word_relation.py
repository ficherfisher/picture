
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import user_relavtion
cookie = 'WEIBOCN_FROM=1110006030;_T_WM=5d8f0642af1d4bebb9a0a49f7cdedecb;M_WEIBOCN_PARAMS=uicode%3D20000174;SUB=_2A25xTst1DeRhGeBH7VcU8i_MyT2IHXVSsNU9rDV6PUJbktBeLRX7kW1NQaiP5mdrF6AsVE8iCD9yVwPK-EbM-DlS;MLOGIN=1;SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whupz6W-ikDAYOPkJhy1.3U5JpX5KzhUgL.Foq4So-feo27eo22dJLoIE-LxKMLBK-L1h2LxK-LBo5L12qLxKMLB.2LBK5LxKMLB.zL1KSk;SUHB=0C1CwuFBF5S0Gw;SSOLoginState=1548401445;XSRF-TOKEN=25d397'

def search():
    key_word = input("请输入用户类型：")
    #key_word = "王者荣耀"
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'cookie': 'WEIBOCN_FROM=1110006030;_T_WM=5d8f0642af1d4bebb9a0a49f7cdedecb;M_WEIBOCN_PARAMS=uicode%3D20000174;SUB=_2A25xTst1DeRhGeBH7VcU8i_MyT2IHXVSsNU9rDV6PUJbktBeLRX7kW1NQaiP5mdrF6AsVE8iCD9yVwPK-EbM-DlS;MLOGIN=1;SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whupz6W-ikDAYOPkJhy1.3U5JpX5KzhUgL.Foq4So-feo27eo22dJLoIE-LxKMLBK-L1h2LxK-LBo5L12qLxKMLB.2LBK5LxKMLB.zL1KSk;SUHB=0C1CwuFBF5S0Gw;SSOLoginState=1548401445;XSRF-TOKEN=25d397',
        'Host': 'weibo.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
    }
    counter_temp = 1
    user_relavtion.table_name(key_word)
    while counter_temp <= 5:
        params = {
            'keyword': key_word,
            'page': counter_temp,
        }
        url = 'https://weibo.cn/search/user/?' + urlencode(params)
        try:
            texts = requests.get(url, headers=header).text
            soup1 = BeautifulSoup(texts, 'html.parser')
            links = soup1.find_all('a')
            temp = []
            user = []
            temp_user = []
            for link in links:
                id = link.get('href')
                temp.append(id)
            temp = list(filter(lambda idstr: '/u/' in idstr, temp))
            for a in temp:
                url = "https://weibo.cn" + a
                user.append(url)
            counter = 1
            while counter <= len(user):
                temp_user.append(user[counter])
                counter = counter + 2
            print("\t\tpage:",counter_temp)
            user_relavtion.user_relation(temp_user,cookie)
            counter_temp = counter_temp + 1

        except:
            print("访问网站错误 ！")
            counter_temp = counter_temp + 1
            continue

if __name__ == "__main__":
    search()