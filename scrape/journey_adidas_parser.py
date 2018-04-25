import sys
import requests
from bs4 import BeautifulSoup
import json
import os

PATH = '/home/cdougherty/Documents/ist441_project'

def parse(file, url):

        # create index
	index = 0

	soup = BeautifulSoup(file, 'html.parser')
	for item in soup.find_all('div', class_='product'):

                # create dictionary of data
		data = {}

                # increment index
		index = index + 1

                # get brand
                data['brand'] = 'JOURNEY'

		try:

                    # get url
                    url = 'https://www.journeys.com'+item.find('a',class_='product-img-link')['href']
                    data['url'] = url

                    # get name
                    name = item.find('span',class_='product-name')
                    data['name'] = name.get_text().upper()

                    # get price
                    price = item.find('span', class_= 'og-price')
                    data['reg-price'] = float(price.get_text().replace('$',''))
                    saleprice = item.find('span', class_= 'sale')
                    data['sale-price'] = float(saleprice.get_text().replace('$',''))

                    # calculate shoe price difference
                    if 'sale-price' in data:
                        data['price-diff'] = data['reg-price'] - data['sale-price']
                    else:
                        data['price-diff'] = 0.0

                    with open('journey_adidas.json','a') as f:
                        json.dump({"index":{"_id":index}},f)
                        f.write("\n")
                        json.dump(data, f)
                        f.write("\n")

		except Exception as e:
			e
