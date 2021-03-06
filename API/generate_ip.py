#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 16:20:24 2019

@author: Magnus Xu
"""
import requests
from bs4 import BeautifulSoup as bs 

def split_line(text):
    words = str(text).split('\n')
    result = [word for word in words]
    return result

def ip_list(url):
	head = {
	    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
	    'connection': 'keep-alive'        
	}
	r = requests.get(url, headers = head)
	text = r.text
	soup = bs(text, 'lxml')
	result = split_line(soup)
	return result

def valid_ip(source):
	head = {
	    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
	    'connection': 'keep-alive'        
	}
	valid = []
	for line in source:
		host = line.strip()
		proxy = {
			'http':'http://' + host
			'https':'https://' + host
		}
		try:
			p = requests.get('https://www.cityrealty.com/', headers = head, proxies = proxy, timeout = 4)
			valid.append(proxy)
		except Exception as error:
			print(error)
			continue
	return valid

if __name__ == "__main__":
	# For the ip list auto-generation , use the API: http://www.xiguadaili.com/api
	url = 'http://api3.xiguadaili.com/ip/?tid=559379427226664&num=2000&delay=3'
	result = ip_list(url)
	result = split_line(result)
	valid = valid_ip(result)
