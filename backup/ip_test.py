#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import pandas as pd
import json

head = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'connection': 'keep-alive'        
}

valid = []
index = 1

with open('filepath') as source:
    for line in source:
        host = line.rstrip()
        proxy = {
            'http':'http://' + host,
            'https':'https://' + host
        }
        print('This is number:', index)
        print(proxy)
        index += 1
        try:
            p = requests.get('testwebsite', headers = head, proxies = proxy, timeout = 5)
            valid.append(proxy)
            print('Success!-----------------------------------------')
        except Exception as error:
            print(error)
            continue
        
with open('valid_ip.txt', 'w') as f:
    for item in valid:
        f.write("%s\n" % item)            
