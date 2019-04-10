from iptools import header, dict2proxy
from bs4 import BeautifulSoup as bs
import requests

def parse_items(items):
	ips = []
	for item in items:
		tds = item.find_all('td')
		ip, port, _type = tds[1].text, int(tds[2].text), tds[5].text
		ips.append({
			'ip': ip,
			'port': port,
			'type': _type
		})
	return ips

def check_ip(ip):
	try:
		proxy = dict2proxy(ip)
		url = 'https://www.ipip.net/'
		r = requests.get(url, headers = headers, proxies = pro, timeout = 5)
		r.raise_for_status()
	except:
		return False
	else:
		return True

def get_proxies(index):
	url = 'http://www.xicidaili.com/nt/%d' % index
	r = requests.get(url, headers = headers)
	r.encoding = r.apparent_encoding
	r.raise_for_status()
	soup = bs(r.text, 'lxml')
	items = soup.find_all('tr')[1:]
	ips = parse_items(items)
	good_proxies = []
	for ip in ips:
		if check(ip):
			good_proxies.append(ip)
	return good_proxies
