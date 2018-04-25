# This python file contains functions for parsing
# a puma shoe html page into a JSON object

# Author: Zack
# Last Updated: April 17, 2018

from bs4 import BeautifulSoup
import json
import os
import re

# path to JSON collection
PATH = '/home/cdougherty/Documents/ist441_project'

# parse puma men's running shoes html page
def parse(file, url):

        # create index
        index = 0

        # begin parsing
	soup = BeautifulSoup(file, 'html.parser')
        print(soup)
	for item in soup.find_all('li', class_='product-tile'):

		# create dictionary of data
		data = {}

                # increment index
                index = index + 1

                # get brand
                data['brand'] = 'PUMA'
                print(data['brand'])

		try:
			# get shoe url and image
			anchor = item.find('a', class_='thumb-link')
			data['url'] = anchor.a['href']
                        #data['img'] = anchor.img['src']
                        print(data['url'])

                        # extract name from url
                        name = img.a['title']
                        data['name'] = name
                        print(data['name'])

			#get shoe price
			saleprice = item.find('span', class_='product-sales-price')
			regprice = item.find('span', class_='product-standard-price')
			if regprice.span['data-prevregprice']:
				data['reg-price'] =  regprice.span['data-prevregprice']
                                data['sale-price'] = saleprice.span['data-prevsaleprice']
                        else:
                                data['reg-price'] = saleprice.span['data-prevsaleprice']

                        # calculate shoe price difference
                        if 'sale-price' in data:
                            data['price-diff'] = data['reg-price'] - data['sale-price']
                        else:
                            data['price-diff'] = 0.0

			# append  to JSON document
                        with open('puma.json', 'a') as f:
                            #json.dump({"index":{"_id": index}}, f)
                            #f.write("\n")
                            json.dump(data, f)
                            f.write("\n")

			# print JSON object
			# print(json_data)

		except Exception as e:
			e
