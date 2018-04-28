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
	for item in soup.find_all('div', class_='o-block--related-product__product-card col-sm-1 col-md-3 col-lg-3'):

            #create dictionary of data
            data = {}

            # increment index
            index = index + 1

            # get brand
            data['brand'] = 'BROOKS'

            try:
                # get url
                data['url'] = item.a['href']

                # get shoe name
                shoe = item.find('div', class_='product__box js-click')
                data['name'] = shoe['data-itemname'].upper()

                # get image
                image = item.find('a', class_='card__slider')
                data['img'] = image.img['data-src']

                # get shoe price
                price = item.find('p', class_='o-block--related-product__product-card__price small')
                if price.find('span', class_='small small--strike') == None:
                    data['reg-price'] = float(price.get_text().replace('$',''))
                else:
                    sale_price = price.find('span', class_='small small--red')
                    data['sale-price'] = float(sale_price.get_text().replace('$',''))
                    reg_price = price.find('span', class_='small small--strike')
                    data['reg-price'] = float(reg_price.get_text().replace('$',''))

                # calculate shoe price difference
                if 'sale-price' in data:
                    data['price-diff'] = data['reg-price'] - data['sale-price']
                else:
                    data['price-diff'] = 0.0

                with open('brooks.json','a') as f:
                    #json.dump({"index":{"_id":index}},f)
                    #f.write("\n")
                    json.dump(data, f)
                    f.write("\n")

            except Exception as e:
                    e
