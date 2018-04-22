# This python file contains functions for parsing
# an sketchers running shoe html page into a JSON object

# Author: Connor Dougherty
# Last Updated: April 22, 2018

from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import json
import os
import re

# path to JSON collection
PATH = '/home/cdougherty/Documents/ist441_project'

# parse sketchers running men's running shoes html page
def parse(file, url):

        # create index
        index = 0

        # begin parsing
	soup = BeautifulSoup(file, 'html.parser')

        for item in soup.find_all('div', class_='product-component js-collectionname-wrapper'):

            try:
                # create dictionary of data
                data = {}

                # increment index
                index = index + 1

                # get brand
                data['brand'] = 'SKETCHERS'

                # get shoe url
                url = item['data-clicked-style-url']
                data['url'] = "https://www.sketchers.com" + url

                # get shoe name
                name = item.find('p', class_='product-name').get_text()
                data['name'] = name.upper()

                # get shoe price
                if item.find('p', class_='price') != None:
                    data['reg-price'] =  float(item.find('p', class_='price').get_text().replace('$',''))
                else:
                    data['sale-price'] = float(item.find('ins', class_='price').get_text().replace('$',''))
                    data['reg-price'] = float(item.find('del', class_='original-price').get_text().replace('$',''))

                # append  to JSON document
                with open('sketchers.json', 'a') as f:
                    json.dump({"index":{"_id": index}}, f)
                    f.write("\n")
                    json.dump(data, f)
                    f.write("\n")

            except Exception as e:
                    e
