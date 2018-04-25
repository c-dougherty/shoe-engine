# This python file contains functions for parsing
# a nike shoe html page into a JSON object

# Author: Connor Dougherty
# Last Updated: April 4, 2018

from bs4 import BeautifulSoup
import json
import os
import re

# path to JSON collection
PATH = '/home/cdougherty/Documents/ist441_project'

# parse nike men's running shoes html page
def parse(file, url):

        # create index
        index = 0

        # begin parsing
	soup = BeautifulSoup(file, 'html.parser')
	for item in soup.find_all('div', class_='grid-item-content'):

		# create dictionary of data
		data = {}

                # increment index
                index = index + 1

                # get brand
                data['brand'] = 'NIKE'

		try:
			# get shoe url and image
			img = item.find('div', class_='grid-item-image')
			data['url'] = img.a['href']
                        # data['img'] = img.img['src']

                        # extract name from url
                        name = img.a['href'].split("/pd/")
                        if len(name) == 1:
                            name = img.a['href'].split("/t/")
                        name = re.split('-\w+-running-', name[1])
                        name = name[0].replace("-"," ")
                        name = name.upper()
                        data['name'] = name

			#get shoe price
			price = item.find('a', class_='color-chip')
			if price['data-op']:
				data['reg-price'] =  float(price['data-op'].replace('$',''))
                                data['sale-price'] = float(price['data-lp'].replace('$',''))
                        else:
                                data['reg-price'] = float(price['data-lp'].replace('$',''))

                        # calculate shoe price difference
                        if 'sale-price' in data:
                            data['price-diff'] = data['reg-price'] - data['sale-price']
                        else:
                            data['price-diff'] = 0.0

			# append  to JSON document
                        with open('nike.json', 'a') as f:
                            #json.dump({"index":{"_id": index}}, f)
                            #f.write("\n")
                            json.dump(data, f)
                            f.write("\n")

			# print JSON object
			# print(json_data)

		except Exception as e:
			e
