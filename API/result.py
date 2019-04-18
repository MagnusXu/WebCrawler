#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 15:37:53 2019

@author: lordxuzhiyu
"""

# -*- coding: utf-8 -*-

import requests
import json
import math
import numpy as np
import pandas as pd

df = pd.read_csv('/Users/lordxuzhiyu/Desktop/SELE.csv')

df['bin'] = pd.to_numeric(df['bin'], errors = 'coerce')

dic1 = df.set_index('bin').to_dict('index')

df2 = pd.read_csv('/Users/lordxuzhiyu/Desktop/new.csv')

dic2 = df2.set_index('Bin').to_dict('index')

seleSet = set(dic1)
newSet = set(dic2)

num = 0

data = pd.DataFrame()


for val in newSet:
    val = float(val)

res = seleSet.intersection(newSet)

for bins in seleSet.intersection(newSet):
    if dic1[bins]['unit'] == dic2[bins]['Unit']:
        data.loc[num, 'address'] = dic2[bins]['Address']
        data.loc[num, 'bin'] = bins
        data.loc[num, 'property_id'] = dic1[bins]['property_id']
        data.loc[num, 'bedroom'] = dic2[bins]['Bedroom']
        data.loc[num, 'full ba'] = dic2[bins]['Full Ba']
        data.loc[num, 'half ba'] = dic2[bins]['Half Ba']
        data.loc[num, 'sq ft'] = dic2[bins]['SqFt']
        num += 1
    
data.to_csv('/Users/lordxuzhiyu/Desktop/result.csv')

