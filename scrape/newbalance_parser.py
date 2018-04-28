# This python file contains functions for parsing
# an newbalance running shoe html page into a JSON object

# Author: Connor Dougherty
# Last Updated: April 22, 2018

from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import json
import os
import re

# path to JSON collection
PATH = '/home/cdougherty/Documents/ist441_project'

# parse new balance running men's running shoes html page
def parse(file, url):

        # create index
        index = 0

        # begin parsing
	soup = BeautifulSoup(file, 'html.parser')

        for item in soup.find_all('div', class_='product product-tile'):

            try:
                
                # create dictionary of data
                data = {}

                # increment index
                index = index + 1

                # get brand
                data['brand'] = 'NEW BALANCE'

                # get shoe url
                url = item.a['href']
                data['url'] = url

                # get shoe name
                name = item.find('p', class_='product-name')
                name = name.a['title']
                data['name'] = name.upper()

                # get image
                data['img'] = item.img['data-original']

                # get shoe price
                price = item.find('div', class_='product-pricing')
                if price.find('span', class_='sales') == None:
                    data['reg-price'] =  float(price.get_text().replace('$',''))
                else:
                    sale_price = price.find('span', class_='sales').get_text()
                    data['sale-price'] = float(re.findall('\d+\.\d+', sale_price)[0])
                    reg_price = price.find('span', class_='reg').get_text()
                    data['reg-price'] = float(re.findall('\d+\.\d+', reg_price)[0])

                # calculate shoe price difference
                if 'sale-price' in data:
                    data['price-diff'] = data['reg-price'] - data['sale-price']
                else:
                    data['price-diff'] = 0.0

                # append  to JSON document
                with open('newbalance.json', 'a') as f:
                    #json.dump({"index":{"_id": index}}, f)
                    #f.write("\n")
                    json.dump(data, f)
                    f.write("\n")

            except Exception as e:
                    e
