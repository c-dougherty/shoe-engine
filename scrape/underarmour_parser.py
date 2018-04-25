from bs4 import BeautifulSoup as soup
import json
import os
import re


def parse(file, url):

    index = 0

    page_soup = soup(file, "html.parser")
    containers = page_soup.find('ul', class_='tileset stack-0')
    containers_li = containers.findAll("li")
    for tile_tile in containers_li:
            
        try:
        
                data = {}
                
                index = index + 1
                
                data['brand'] = 'UNDERARMOUR'
                
                url = tile_tile.a['href']
                data['url'] = url
                
                product_name = tile_tile.find("div",{"class":"title"})
                name = product_name.text.encode('ascii', 'replace')
                name = name.replace("?", "")
                data['name'] = name.upper()
                
                price = tile_tile.find("div",{"class":"price-detail"})
                sale = price.find("span",{"class":"price-red"})
                if sale == None:
                    data['reg-price'] = float(price.text.replace('$',''))
                else:
                    sale_price = sale.find("span",{"class":"price-sale"})
                    price_orig = sale.find("span",{"class":"price-orig"})
                    data['sale-price'] = float(sale_price.text.replace('$',''))
                    data['reg-price'] = float(price_orig.text.replace('$',''))
                
                # calculate shoe price difference
                if 'sale-price' in data:
                    data['price-diff'] = data['reg-price'] - data['sale-price']
                else:
                    data['price-diff'] = 0.0

                with open('underarmour.json', 'a') as f:
                    #json.dump({"index":{"_id": index}}, f)
                    #f.write("\n")
                    json.dump(data, f)
                    f.write("\n")


        except Exception as e:
            e
