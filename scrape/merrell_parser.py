from bs4 import BeautifulSoup as soup
import json
import os
import re

PATH = '/home/cdougherty/Documents/ist441_project'

def parse(file, url):

    index = 0

    page_soup = soup(file, "html.parser")
    containers = page_soup.findAll("div",{"class":"product-tile"})


    for container in containers:
            
        try:
        
                data = {}
                
                index = index + 1
                
                data['brand'] = 'MERRELL'
                #print(data['brand'])
                
                url = container.a['href']
                data['url'] = url
                #print(data['url'])
                
                product_name = container.a['title']
                data['name'] = product_name.upper()
                #print(data['name'])
                
                if container.find("span",{"class":"product-standard-price"}) == None:
                        #print("no sale")
                        price = container.span.text.strip()
                        data['reg-price'] = float(price.replace('$',''))
                else:
                        #print("sale")
                        sale_price = container.find("span",{"class":"product-sales-price"})
                        data['sale-price'] = float(sale_price.text.replace('$',''))
                        reg_price = container.find("span",{"class":"product-standard-price"})
                        data['reg-price'] = float(reg_price.text.replace('$',''))
                
                # calculate shoe price difference
                if 'sale-price' in data:
                    data['price-diff'] = data['reg-price'] - data['sale-price']
                else:
                    data['price-diff'] = 0.0

                with open('merrell.json', 'a') as f:
                    json.dump({"index":{"_id": index}}, f)
                    f.write("\n")
                    json.dump(data, f)
                    f.write("\n")


        except Exception as e:
            e
