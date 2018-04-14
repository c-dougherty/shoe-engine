from json import dumps
import os
from elasticsearch import Elasticsearch, helpers
import sys, json

#path to JSON collection
path='/home/cdougherty/Documents/ist441_project/scrape'

#User credentials
USER='elastic'
PASSWORD='l1on5#441H34D'

#Choose a name for your index and an ad hoc document type
INDEX_NAME='shoe-prices'
DOCTYPE='doc'

#Configuring connection parameters
es = Elasticsearch(
        ['localhost'],
        http_auth=(USER,PASSWORD),
        scheme="http",
        port=9200
)

#To avoid loading everything in memory, we use a generator
def load_json(directory):

	for filename in os.listdir(directory):
		if filename.endswith('.json'):
			with open(os.path.join(directory, filename), 'r') as open_file:
                            for line in open_file:
				yield json.loads(line)

#Indexing in Elastic via bulk load
helpers.bulk(es, load_json(path), index=INDEX_NAME, doc_type=DOCTYPE)
