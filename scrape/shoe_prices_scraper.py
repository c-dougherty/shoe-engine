# This script crawls a list of documents,
# scrapes the shoe price information, and
# dumps the information into JSON documents

# Author: Connor Dougherty
# Last Updated: March 20, 2018

import sys
import requests
import nike_parser
import altra_parser
import puma_parser
import merrell_parser
import underarmour_parser
import newbalance_parser
import skechers_parser
import brooks_parser
import journey_adidas_parser
import saucony_parser

def fetch(url):
  try:
    return requests.get(url)
  except IOError:
    print('problem reading url:', url)


def main():

	# fetch html pages

        newbalance_url = "http://www.newbalance.com/men/shoes/running/"
        r = fetch(newbalance_url)
        newbalance_parser.parse(r.text, r.url)

        skechers_url = "https://www.skechers.com/en-us/men/styles/shoes/performance"
        r = fetch(skechers_url)
        skechers_parser.parse(r.text, r.url)

        nike_url = "https://store.nike.com/us/en_us/pw/mens-running-shoes/7puZ8yzZoi3"
	r = fetch(nike_url)
	nike_parser.parse(r.text, r.url)

        merrell_url = 'https://www.merrell.com/US/en/mens-trail-running/'
        r = fetch(merrell_url)
        merrell_parser.parse(r.text, r.url)

        underarmour_url = 'https://www.underarmour.com/en-us/mens/footwear/running/g/39rha'
        r = fetch(underarmour_url)
        underarmour_parser.parse(r.text, r.url)

        altra_url = "https://www.altrarunning.com/running-shoes/men"
        r = fetch(altra_url)
        altra_parser.parse(r.text, r.url)

	brooks_url = "http://www.brooksrunning.com/en_us/all-mens-running-shoes/?start=0"
        r = fetch(brooks_url)
	brooks_parser.parse(r.text, r.url)

	journey_adidas_url = "https://www.journeys.com/search?keywords=mens%20shoes&gender=Men&ref=jy_visnav_mens&brand=Adidas&category=Running%20Shoes"
        r = fetch(journey_adidas_url)
	journey_adidas_parser.parse(r.text, r.url)

        #puma_url = "https://us.puma.com/en_US/men/shoes/runningtraining"
        #r = fetch(puma_url)
        #puma_parser.parse(r.text, r.url)

        #saucony_url = "https://www.saucony.com/en/mens-running-sale/"
        #r = fetch(saucony_url)
        #saucony_parser.parse(r.text, r.url)

if __name__ == '__main__':
    main()
