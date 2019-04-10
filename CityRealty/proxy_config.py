import requests
import re
from config import *
import json
import pandas as pd
from pandas.io.json import json_normalize

url = "https://www.cityrealty.com/"
headers = {
	"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
	"Cookie":""
	# I don't know where you store cookies
}

proxy_dic_list = {}
num_lines = 0
lines = []

proxy_list = pd.DataFrame()

http = []
https = []
ftp = []
col_name = ['http', 'https', 'ftp']

with open('proxy-list.txt') as source:
    for line in source:
        data = json.loads(line)
        host = data['host']
        http_proxy = "http://" + host + ":80"
        https_proxy = "https://" + host + ":443"
        ftp_proxy = "ftp://" + host + ":21"
        proxy_dict = {
                "http": http_proxy,
                "https": https_proxy,
                "ftp": ftp_proxy
        }
        http.append(http_proxy)
        https.append(https_proxy)
        ftp.append(ftp_proxy)
        #print(proxy_dict)
        #nn = json_normalize(data['host'])
        num_lines += 1
        lines.append(proxy_dict)
        proxy_list.append(proxy_dict, ignore_index = True)
        proxy_dic_list.update(proxy_dict)

df = pd.DataFrame([http, https, ftp]).T
df.columns = ['http', 'https', 'ftp']
print(df)
#print(pd.DataFrame.from_dict(lines, orient = 'index'))
