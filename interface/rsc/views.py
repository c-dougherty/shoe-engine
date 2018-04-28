from django.http import HttpResponse
from django.shortcuts import render
from models import *
from django.template.context import RequestContext
import settings
from django.shortcuts import get_object_or_404
import requests
from settings import *
from manage import * 
from elasticsearch import Elasticsearch, helpers

ERR_QUERY_NOT_FOUND='<h1>Query not found</h1>'
ERR_IMG_NOT_AVAILABLE='The requested result can not be shown now'

#User credentials
USER='elastic'
PASSWORD='l1on5#441H34D'

#Specify elastic index name
ELASTIC_INDEX='shoe-prices'

#Configuring connection parameters
es = Elasticsearch(
                ['localhost'],
                http_auth=(USER,PASSWORD),
                scheme="http",
                port=9200
)

def home(request):
    if request.method == 'POST':
        q = request.POST.get('q',None)
        start=request.POST.get('start',0)
        if q != None and len(q) > 2:
            return search(request,q,start)
        else:
            if q==None:
                return render(request, 'rsc/index.html',{'errormessage':None})
            else:
                errormessage='Please use larger queries'
                return render(request, 'rsc/index.html',{'errormessage':errormessage})
    else: 
        # it's a get request, can come from two sources. if start=0, or start not in GET dictionary, someone is requesting the page 
        # for the first time 
   
        start=int(request.GET.get('start',0))
        query=request.GET.get('q',None)
        if start==0 or query==None:
            return render(request, 'rsc/index.html')
        else:
            return search(request,query,start)
                

def search(request,query,start):
     
       # set query result size
       size = 50

       # check for keywords in query
       if " AND " in query:
           # split query and perform boolean search
           #terms = query.split(' AND ')
           #res = es.search(index=ELASTIC_INDEX, body= {"from": start, "size": size, "query":{"bool": {"must": {"multi_match":{"query": terms[0], "fields": ["brand", "name"]}}, "must": {"multi_match":{"query": terms[1], "fields": ["brand", "name"]}}}}, "sort":[{"price-diff":{"order":"desc"}}, {"reg-price":{"order":"asc"}}]})
           terms = query.replace(' AND ', ' ')
           res = es.search(index=ELASTIC_INDEX, body= {"from": start, "size": size, "query":{"multi_match":{"query": terms, "type": "cross_fields", "fields": ["brand", "name"], "operator": "and"}}, "sort":[{"price-diff":{"order":"desc"}}, {"reg-price":{"order":"asc"}}]})
       elif query == "ALL":
           res = es.search(index=ELASTIC_INDEX, body= {"from": start, "size": size, "query":{"match_all": {}}, "sort":[{"price-diff":{"order":"desc"}},{"reg-price":{"order":"asc"}}]})
       else:
           res = es.search(index=ELASTIC_INDEX, body= {"from": start, "size": size, "query":{"multi_match":{"query": query, "fields": ["brand", "name"]}}, "sort":[{"price-diff":{"order":"desc"}}, {"reg-price":{"order":"asc"}}, "_score"]})

       if not res.get('hits'):

            return render(request, 'rsc/error.html',{'errormessage':'Your query returned zero results, please try another query'})
        
         
       else:
            print "search done"
            totalresultsNumFound= res['hits']['total']
            results=res['hits']['hits']
            SearchResults=[] 
            if len(results) > 0:
                for result in results:

                    resultid= result['_id'] 
                    f = SearchResult(resultid) #calling the object class that is defined inside models.py

                    if 'sale-price' in result['_source']:
                        f.content= result['_source']['reg-price'] - result['_source']['sale-price']
                    else:
                        f.content= 0.0

                    # get image
                    if 'img' in result['_source']:
                        f.image = result['_source']['img']
                    else:
                        f.image = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/LoCos_Question.svg/200px-LoCos_Question.svg.png"
                    
                    # get url 
                    url = result['_source']['url']
                    f.url = url.split('//')[1]     # remove web protocol from url

                    # get brand and shoe name
                    f.title = result['_source']['brand'] + " " + result['_source']['name']

                    # get shoe price info
                    if 'sale-price' in result['_source']:
                        f.description = "Price Difference: $" + str(result['_source']['reg-price'] - result['_source']['sale-price']) + ", Sale price: $" + str(result['_source']['sale-price']) + ", Regular price: $" + str(result['_source']['reg-price'])
                    else:
                        f.description = "Price: $" + str(result['_source']['reg-price'])

                    SearchResults.append(f)
                
                #SearchResults.sort(key=lambda f: f.content, reverse=True)
                return render(request, 'rsc/htmlresult.html', {'results':SearchResults ,'q': query,\
							  'total':totalresultsNumFound, 'i':str(start+1)\
							  , 'j':str(len(results)+start) })
            else:
               return render(request,'rsc/error.html',{'errormessage':'Your search returned zero results, please try another query'})
				
	


