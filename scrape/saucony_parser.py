# This python file contains functions for parsing
# a saucony shoe html page into a JSON object

# Author: Connor Dougherty
# Last Updated: March 28, 2018

from bs4 import BeautifulSoup
import json
import os

# path to JSON collection
PATH = '/home/cdougherty/Documents/ist441_project'

# parse saucony men's running shoes html page
def parse(file, url):

        # create JSON document
        #json_doc = []

        # create index
        index = 1

        # begin parsing
	soup = BeautifulSoup(file, 'html.parser')
	for item in soup.find_all('div', class_='product-tile'):

		# create dictionary of data
		data = {}

                # get url
                data['url'] = url

		try:
			# get shoe name
			name = item.find('div', class_='product-name')
			data['name'] = name.meta['content']

			#get shoe prices
			price = item.find('div', class_='product-pricing')
                        sale_price = price.find('span', class_='product-sales-price')
			data['sale-price'] = sale_price.get_text()
                        reg_price = price.find('span', class_='product-standard-price')
			data['reg-price'] = reg_price.get_text()

                        # calculate shoe price difference
                        if 'sale-price' in data:
                            data['price-diff'] = data['reg-price'] - data['sale-price']
                        else:
                            data['price-diff'] = 0.0

			# append  to JSON document
                        with open('saucony.json', 'a') as f:
                            json.dump({"index":{"_id": index}}, f)
                            f.write("\n")
                            json.dump(data, f)
                            f.write("\n")

                        # increment index
                        index = index + 1

		except Exception as e:
			e
