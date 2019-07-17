from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
def getCookies(username,password):
    Dirver = webdriver.Chrome()#chrome驱动对象
    Dirver.get("https://passport.weibo.cn/signin/login?")#打开登录网页
    loginName = WebDriverWait(Dirver,10).until(EC.visibility_of_element_located((By.ID, "loginName")))
    #驱动chrome浏览器，等待10秒，直到在网页源代码中找到属性为<... id = "loginName">
    loginPassword = Dirver.find_element_by_id("loginPassword")#找到属性为<... id = "loginPassword">
    loginName.send_keys(username)
    time.sleep(1)
    loginPassword.send_keys(password)
    time.sleep(1)
    #往H5标签中的text填入账号，密码
    loginLink = Dirver.find_element_by_link_text('登录')
    ActionChains(Dirver).move_to_element(loginLink).click().perform()
    #找到登录标签，执行点击动作
    time.sleep(10)
    #等待10s，进入身份验证界面
    loginButton = Dirver.find_element_by_id("embed-captcha")
    loginButton.click()
    #点击验证按钮
    time.sleep(8)
    cookies = Dirver.get_cookies()
    Dirver.close()
    tempcookie = []
    for cookie in cookies:
        temp = cookie['name'] + '=' + cookie['value']
        tempcookie.append(temp)
        #找到cookie标签和对应的值，并整合到一起
    tempcookie = ';'.join(tempcookie)
    #加入分号，以便区别
    return tempcookie
def Save(cookie):
    with open("D:/python/crawl/crawlWengDang/WeiboCookie/cookies.txt","a") as f:
        f.write(cookie)
        f.write('\n')

if __name__ == "__main__":
    with open("D:/python/crawl/crawlWengDang/WeiboCookie/UserInfor.txt","r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()#删除换行符
            username = line.split("-")[0]
            password = line.split("-")[1]
            cookie = getCookies(username,password)
            if cookie == None:
                print("cookie获取失败！")
            else:
                Save(cookie)
                print(username + "  cookie获取成功！")