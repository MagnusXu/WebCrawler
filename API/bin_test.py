#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 10:42:57 2019

@author: lordxuzhiyu
"""

import requests
import json

#url = 'https://api.cityofnewyork.us/geoclient/v1/address.json?houseNumber=207&street=E 74th St&borough=manhattan&app_id=35348ee9&app_key=874bc0a8aaafe29bbe84abaeb78fd57d'
#/v1/address.json?houseNumber=PHA&street=207 East 74th Street&borough=manhattan&app_id=abc123&app_key=def456

head = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'connection': 'keep-alive'        
}

str1 = '207 E 74th St'
listing = str1.split(' ')

num = listing[0]

del(listing[0])

street = ' '.join(listing)

url = 'https://api.cityofnewyork.us/geoclient/v1/address.json?houseNumber=' + num + '&street=' + street + '&borough=manhattan&app_id=35348ee9&app_key=874bc0a8aaafe29bbe84abaeb78fd57d'


r = requests.get(url, headers = head)
#print("Status Code:", r.status_code)

rjson = r.json()
rjson = json.dumps(rjson)
json_dict = json.loads(rjson)

bins = json_dict['address']['buildingIdentificationNumber']
print(bins)
