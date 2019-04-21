#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 15:37:53 2019
@author: Magnus Xu
"""

# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd

def list_pre_processing(dataset_path):
    df = pd.read_csv(dataset_path)
    df.reset_index(drop = True)
    df = df.drop(['Unnamed: 0'],axis = 1)
    return df

def get_address_info(df, column_name):
    """
    # This is used for spliting the address into street name, street number, unit number
    # e.g. For the address: 207 E 74th St, Unit PHA, we want to split it into three variables. 
    # street_number: 207
    # street_name: E 74th St
    # unit: PHA
    """
    address = df[column_name]
    element = str(address).split(',')
    if len(element) < 2:
        return None
    full_street = element[0]
    unit = element[1]
    unit = unit.replace(' Unit ','')
    l = full_street.split(' ')
    street_number = l[0]
    if !street_number.isdigit():
        return None
    street_name = ' '.join(l[1:])
    dic = {
        'street_number':street_number,
        'street_name':street_name,
        'unit':unit
    }
    return dic

def split_line(text):
    words = text.split(',')
    result = [word for word in words]
    return result

def generate_url(df):
    # The API address is: https://api.cityofnewyork.us/geoclient/v1/doc#home
    # We are using the method 1.2.1-Address
    # Potential issue: The app_id & app_key might needs updates or set as seperate parameter in the input IF WHOEVER READ THIS CODE NEEDS A LIST OF DIFFERENT ID AND KEY IN THE FUTURE, but so far, I just use the same id and key.
    street_number, street_name, unit = get_address_info(df, 'Address')
    url = 'https://api.cityofnewyork.us/geoclient/v1/address.json?houseNumber=' + {} + '&street=' + {} + '&borough=manhattan&app_id=35348ee9&app_key=874bc0a8aaafe29bbe84abaeb78fd57d'.format(street_number, street_name)
    return url

def json_crawler(url):
    head = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'connection': 'keep-alive'        
    }
    r = requests.get(url, headers = head)
    json_dict = json.loads(json.dumps(r.json()))
    return json_dict

def write_address_into_df(index, row, df, json_dict):
    bins = json_dict['address']['buildingIdentificationNumber']
    address = row['Address']
    street_number, street_name, unit = get_address_info(row, 'Address')
    df.loc[index, 'Address'] = address
    df.loc[index, 'Bin'] = bins
    df.loc[index, 'Street Number'] = street_number
    df.loc[index, 'Street'] = street_name
    df.loc[index, 'Unit'] = unit
    df.loc[index, 'Bedroom'] = row['Bd']
    df.loc[index, 'Full Ba'] = row['Full Ba']
    df.loc[index, 'Half Ba'] = row['Half Ba']
    df.loc[index, 'SqFt'] = row['Sq Ft']

def generate_crawl_result(dataset_path):
    df = list_pre_processing(dataset_path)
    count = 0
    new_data = pd.DataFrame()
    for index, row in df.iterrows():
        try:
            street_number, street_name, unit = get_address_info(row, 'Address')
            url = generate_url(row)
            json_dict = json_crawler(url)
            try:
                write_address_into_df(index, row, newData, json_dict)
                count += 1
            except Exception as errorInside:
                print('The inner error is:', errorInside)
        except Exception as errorOutside:
            print('The outer error is:', errorOutside)
    print('Total success records is:', count)
    return new_data

def closing_preprocessing(dataset_path):
    df = pd.read_csv(dataset_path, low_memory = False)
    df['bin'] = pd.to_numeric(df['bin'], errors = 'coerce')
    return df

def re_index(df, column_name):
    df.set_index(column_name, inplace = True, drop = False)
    return df

def generate_merge_result(df, df2):
    result = pd.DataFrame()
    count = 0
    for index, row in df2.iterrows():
        val = row['Bin']
        try:
            df1 = df.loc[val]
            if isinstance(df1, pd.Series):
                df1.to_frame()
            for index1, row1 in df1.iterrows():
                unit = row1.loc['unit']
                pro = row1.loc['property_id']
                if unit == row['Unit']:
                    data.loc[count, 'address'] = row['Address']
                    data.loc[count, 'unit'] = uni
                    data.loc[count, 'bin'] = val
                    data.loc[count, 'property_id'] = pro
                    data.loc[count, 'bedroom'] = row['Bedroom']
                    data.loc[count, 'full ba'] = row['Full Ba']
                    data.loc[count, 'half ba'] = row['Half Ba']
                    data.loc[count, 'sq ft'] = row['SqFt']
                    count += 1
        except Exception as error:
            print(error)
            pass
    return result


if __name__ == "__main__":
    listing_path = '/Desktop/Penthouse_Listing_SS.csv'
    crawl_df = generate_crawl_result(listing_path)
    closing_path = '/Desktop/SELE.csv'
    closing_df = closing_preprocessing(closing_path)
    result = generate_merge_result(closing_df, crawl_df)
    result.to_csv('file_path')
