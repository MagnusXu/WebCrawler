import requests
import re
from bs4 import BeautifulSoup
from json import loads, dumps
from config import *
import csv
import datetime
from time import sleep
from random import randint

def test_crawler():
	import pandas as pd
	import time

	headers = {
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
		'cookie': COOKIES[0],
	}
    
    http_proxy = "http://110.52.235.237:80"
    https_proxy = "https://110.52.235.237:443"
    ftp_proxy = "ftp://110.52.235.237:21"
    proxy_dict = {
            "http":http_proxy,
            "https":https_proxy,
            "ftp":ftp_proxy
            }

	fileHeader = ["full_address", 'house_number', 'street', 'unit_number', "sizeft", 'amenities', 'bedroom', 'bathroom']
	
	csvFile = open("res_{}.csv".format(datetime.datetime.now().isoformat()), "w", buffering=BUFF_SIZE)
	writer = csv.writer(csvFile)
	writer.writerow(fileHeader)
	df = pd.read_csv('./query_result.csv')
	df['full_address'] = df['house_number'] + " " + df['street']
	print(df.shape[0])
	
	for row_idx in range(2700):
		s = requests.session()
        
        sleep(randint(20, 40))
		
		row = df.iloc[row_idx]
		if 'nan' in str(row['full_address']):
			continue
		print(row_idx, row['unit_number'])
		try:
			# get cookies
			url = "https://www.cityrealty.com/"
			headers['cookie'] = COOKIES[(row_idx+1) % 3]
			r = s.get(url, headers = headers, proxies = proxyDict)
			
			# query for getting target url
			url = "https://www.cityrealty.com/nyc/search-for-sale/{}?min_price=100000&max_price=50000000000".format(row['full_address'])
			print(url)
			unique_id = round(time.time()*1000)
			r = s.get(url, headers=headers)            
			
			# match the backend unique id to get target url
			url = "https://www.cityrealty.com/rpc/search/get-sale-listings?f%5B%5D=priceRangeSale&f%5B%5D=location&f%5B%5D=bedroomFullMulti&f%5B%5D=saleBuildingTypeMulti&f%5B%5D=doorman&f%5B%5D=inContract&f%5B%5D=dateListed&f%5B%5D=priceChange&f%5B%5D=searchTermListings&f%5B%5D=subHoods&s%5B%5D=salePrice&s%5B%5D=dateListed&s%5B%5D=ppsqft&s%5B%5D=neighborhood2&s%5B%5D=type2&s%5B%5D=registration&type=json&uniqueid={}".format(unique_id)
			r = s.get(url, headers=headers)
		except Exception as e:
			print(e)
			
		try:
			# get the target url
			new_url = '{}{}'.format(CITY_REALTY_URL_PREFIX, loads(r.text)['items'][0].get('url_listing'))
#            print([item.get('unit') for item in loads(r.text)['items']])
			print(new_url)
			r = s.get(new_url, headers=headers)
			
			soup = BeautifulSoup(r.text, "html.parser")
			all_closing_history_url = '{}{}'.format(CITY_REALTY_URL_PREFIX, soup.find('div', {'id':'recent_closings'})['data-rpc'].split('?')[0])
			print(all_closing_history_url)
			
			r = s.get(all_closing_history_url, headers=headers)
			soup = BeautifulSoup(r.text, "html.parser")
			query = {
				'class':'tr',
				'data-unit': row['unit_number'],
			}
			unit_object = soup.find('div', query)
			if unit_object == None:
				print('unit_number not found.')
				print('==============================')
				continue
			unit_price = unit_object['data-price']
			unit_sizeft = unit_object['data-sizeft']
			unit_room_info_split = unit_object.find('div', {'class':'td size'}).get_text().replace('s','').split()[::-1]
			room_info = {}
			for idx, tmp in enumerate(unit_room_info_split):
				if idx % 2 == 0:
					room_info[tmp] = unit_room_info_split[idx+1]
				else:
					continue
			
			unit_url = '{}{}'.format(CITY_REALTY_URL_PREFIX, unit_object.find('div', {'class':"td unit"}).find('a')['href'])
			r = s.get(unit_url, headers=headers)
			soup = BeautifulSoup(r.text, "html.parser")
			amenities = ','.join([amenity.strip() for amenity in soup.find('ul',{"class":"w_list"}).get_text().split('\n') if amenity != ""])
			print([row['full_address'], row['house_number'], row['street'], unit_sizeft, amenities, room_info.get('bed'), room_info.get('bath')])
			
			writer.writerow([row['full_address'], row['house_number'], row['street'], row['unit_number'], unit_sizeft, amenities, room_info.get('bed'), room_info.get('bath')])
			if row_idx % 20 == 0:
				csvFile.flush()
		except Exception as e:
			print(e)
		print("========================================")
        
			
			
	csvFile.close()
		
if __name__ == '__main__':
	test_crawler()
