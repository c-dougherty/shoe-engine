# This python file contains functions for parsing
# an altra running shoe html page into a JSON object

# Author: Connor Dougherty
# Last Updated: April 16, 2018

from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import json
import os
import re

# path to JSON collection
PATH = '/home/cdougherty/Documents/ist441_project'

# parse altra running men's running shoes html page
def parse(file, url):

        # create index
        index = 0

        # begin parsing
	soup = BeautifulSoup(file, 'html.parser')

        for item in soup.find_all('div', class_='product-content'):

            try:
                
                # create dictionary of data
                data = {}

                # increment index
                index = index + 1

                # get brand
                data['brand'] = 'ALTRA RUNNING'

                # get shoe url
                url = item.find('a', class_='product-link')
                data['url'] = "https://www.altrarunning.com" + url['href']

                # skip item if not men's shoes
                skip = False
                if url['href'].find("men") < 0:
                    skip = True
                if url['href'].find("apparel") >= 0:
                    skip = True

                # get shoe name
                name = url.h3.get_text()
                name = name.encode('ascii', 'replace')
                name = name.replace("?", "'")
                data['name'] = name.upper()

                # get shoe price
                price = item.find('div', class_='sale-price')
                if price.find('div', class_='sale') == None:
                    data['reg-price'] =  float(price.div.get_text().replace('$',''))
                else:
                    data['sale-price'] = float(price.find('div', class_='sale').get_text().replace('$',''))
                    data['reg-price'] = float(price.find('div', class_='has-sale').get_text().replace('$',''))

                # calculate shoe price difference
                if 'sale-price' in data:
                    data['price-diff'] = data['reg-price'] - data['sale-price']
                else:
                    data['price-diff'] = 0.0

                # skip item if duplicate
                #try:
                #    with open('altra.json', 'r') as f:
                #        for line in f:
                #            print(line)
                #            j = json.load(line)
                #            if data == j:
                #                skip = True
                #except Exception as ex:
                #    ex

                # append  to JSON document
                if not skip:
                    with open('altra.json', 'a') as f:
                        #json.dump({"index":{"_id": index}}, f)
                        #f.write("\n")
                        json.dump(data, f)
                        f.write("\n")

            except Exception as e:
                    e
