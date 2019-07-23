import requests
from multiprocessing.dummy import Pool as ThreadPool
import os
pool = ThreadPool(10)
aliveIp = []
def CheckAlive(proxy):
    proxies = {'http':proxy}
    try:
        if requests.get('https://www.baidu.com',proxies = proxies,timeout = 3).status_code == 200:
            print("代理：{}存活".format(proxy))
            aliveIp.append(proxy)
    except:
        print("代理：{}失败".format(proxies))

def SaveFile():
    with open(os.getcwd()+"/data/alive.txt","a+") as f:
        for ip in aliveIp:
            f.write(ip+"\n")
    print("save success")

def Main():
    with open(os.getcwd()+"/data/IpPool.txt",'r') as f:
        lines = f.readlines()
        proxies = list(map(lambda x:x.strip(),[y for y in lines]))
        pool.map(CheckAlive,proxies)
        SaveFile()
if __name__ == "__main__":
    Main()