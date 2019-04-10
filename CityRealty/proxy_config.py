import requests
import re
import json

url = "https://www.cityrealty.com/"
headers = {
	"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
	"Cookie":""
	# I don't know where you store cookies
}

proxy_dic_list = {}
num_lines = 0
# Save all proxy object in proxy_dic_list
with open('proxy-list.txt') as source:
    for line in source:
        data = json.load(line)
        host = data['host']
        http_proxy = "http://" + host + ":80"
        https_proxy = "https://" + host + ":443"
        ftp_proxy = "ftp://" + host + ":21"
        proxy_dict = {
                "http": http_proxy,
                "https": https_proxy,
                "ftp": ftp_proxy
        }
        print(proxy_dict)
        num_lines += 1
        proxy_dic_list[num_lines].append(proxy_dict)
	
r = requests.get(url, headers = headers, proxies = proxy_dict)
