# This script crawls a list of documents,
# scrapes the shoe price information, and
# dumps the information into JSON documents

# Author: Connor Dougherty
# Last Updated: March 20, 2018

import sys
import requests
import nike_parser
import altra_parser
import saucony_parser

def fetch(url):
  try:
    return requests.get(url)
  except IOError:
    print('problem reading url:', url)


def main():

	# fetch html pages
        nike_url = "https://store.nike.com/us/en_us/pw/mens-running-shoes/7puZ8yzZoi3"
	r = fetch(nike_url)
	nike_parser.parse(r.text, r.url)

        altra_url = "https://www.altrarunning.com/running-shoes/men"
        r = fetch(altra_url)
        altra_parser.parse(r.text, r.url)

#        saucony_url = "https://www.saucony.com/en/mens-running-sale/"
#        r = fetch(saucony_url)
#        saucony_parser.parse(r.text, r.url)

if __name__ == '__main__':
    main()
