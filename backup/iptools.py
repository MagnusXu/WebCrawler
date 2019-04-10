import json
 
import requests
import time
import pymysql
from iptools import header, dict2proxy
from bs4 import BeautifulSoup as Soup
from pymongo import MongoClient as Client
import threading
import random

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/64.0.3282.186 Safari/537.36'}
 
def dict2proxy(dic):
    s = dic['type'] + '://' + dic['ip'] + ':' + str(dic['port'])
    return {'http': s, 'https': s}

def get_user_agent():
    '''
    功能: 随机获取UA
    :return: 返回一个随机UA
    '''
    user_agents=[
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]
    user_agent = random.choice(user_agents)
    return user_agent



def parse_items(items):
    # 存放ip信息字典的列表
    ips = []
    for item in items:
        tds = item.find_all('td')
        # 从对应位置获取ip，端口，类型
        ip, port, _type = tds[1].text, int(tds[2].text), tds[5].text.lower()
        ips.append({'ip': ip, 'port': port, 'type': _type})
 
    return ips

def check_ip(ip, good_proxies):#检查ip是否可以用
    try:
        pro = dict2proxy(ip)
        # print(pro)
        url = 'https://www.ipip.net/'
        r = requests.get(url, headers=header, proxies=pro, timeout=5)
        r.raise_for_status()
    except Exception as e:
        # print(e)
        pass
    else:
        good_proxies.append(ip)
        
def write_to_mysql(ips):
    conn = pymysql.connect(host='xx.xx.xx.xx', user='xx', passwd='xxxxxxx', db='xx', charset="utf8")
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    for i in range(len(ips)):
        
          print(ips[i]['ip'])
          query="""insert into pr_ip(ip,port,_type)values(%s,%s,%s)"""
          ip=ips[i]['ip']
          port=ips[i]['port']
          type1=ips[i]['type']
          values=(ip,port,type1)
          print (values,query)
          cursor.execute(query,values)
    cursor.close()
    conn.commit()
    conn.close()

def write_to_json(ips):
    with open('proxies.json', 'w', encoding='utf-8') as f:
        json.dump(ips, f, indent=4)
 
 
def write_to_mongo(ips):
    conn = pymysql.connect(host='xx.xx.xx.xx', user='xx', passwd='xxxxxxxxxxx', db='xx', charset="utf8")
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    for i in range(len(ips)):
        
          print(ips[i]['ip'])
          query="""insert into pr_ip(ip,port,_type)values(%s,%s,%s)"""
          ip=ips[i]['ip']
          port=ips[i]['port']
          type1=ips[i]['type']
          values=(ip,port,type1)
          print (values,query)
          cursor.execute(query,values)
    cursor.close()
    conn.commit()
    conn.close()
 
class GetThread(threading.Thread):
    '''对Thread进行封装'''
    def __init__(self, args):
        threading.Thread.__init__(self, args=args)
        self.good_proxies = []
 
    def run(self):
        url = 'http://www.xicidaili.com/nt/%d' % self._args[0]
        # 发起网络访问
        user_agent = get_user_agent()
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        soup = Soup(r.text, 'lxml')
        # 第一个是显示最上方的信息的，需要丢掉
        items = soup.find_all('tr')[1:]
        ips = parse_items(items)
        threads = []
        for ip in ips:
            # 开启多线程
            t = threading.Thread(target=check_ip, args=[ip, self.good_proxies])
            t.start()
            time.sleep(0.1)
            threads.append(t)
        [t.join() for t in threads]
 
    def get_result(self):
        return self.good_proxies
 
 
if __name__ == '__main__':
    # 主函数使用多线程
    threads = []
    for i in range(1, 30):
        t = GetThread(args=[i])
        t.start()
        time.sleep(3)
        threads.append(t)
    [t.join() for t in threads]
    for t in threads:
        proxies = t.get_result()
        
        write_to_mongo(proxies)
