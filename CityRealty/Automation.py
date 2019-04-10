#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 11:50:12 2019

@author: lordxuzhiyu
"""

from bs4 import BeautifulSoup as bs
import requests

def combine_url(url1, url2):
    return '%s%s' % (url1, url2)

def get_soup(url):
    html = requests.get(url)
    txt = html.text
    soup = bs(txt, 'lxml')
    return soup

def get_basic_info(soup, unit):
    for i in soup.find_all(attrs = {"data-unit":unit}):
        size = i.find(attrs = {"class":"td size"}).get_text()
        ft = i.find(attrs = {"class":"td size_ft"}).get_text()
        price = i.find(attrs = {"class":"td price"}).get_text()
        print(unit, size, ft, price)
        
def get_href(soup, unit):
    for i in soup.find_all(attrs = {"data-unit":unit}):
        for j in i.find_all('a'):
            href = j.get('href')
            if href is not None:
                return href
            
def get_amenity(soup):
    for i in soup.find_all(attrs = {"class":"w_list"}):
        print(i.get_text())
        
base = 'https://www.cityrealty.com'
source = 'nyc/beekman-sutton-place/447-east-57th-street/closing-history/3525'
source_url = combine_url(base, source)
source_soup = get_soup(source_url)

get_basic_info(source_soup, 'PH')
