#!/usr/bin/env python

from pprint import pprint

import json

import http.client, urllib.parse


def http_get(connection, path):
 dict = {}
 dict['KEY'] = 'EE20JKBHtxwSIZrgLQvcntLC3CpUcOW5BYXT93Qu'

 #dict['filters'] = '{"category":"health & medicine"}'
 dict['q'] = 'Neomycin'
 

 connection.request('GET', path + '?' + urllib.parse.urlencode(dict))

 response = connection.getresponse()

 if response.status == 200:

   data = response.read() #will be in bytes

   return json.loads(data.decode('utf-8'))

 else:

   raise Exception("HTTP call failed: " + response.reason)

 

url = 'api.v3.factual.com' #API

connection = http.client.HTTPSConnection(url) #create connection


# get the children of the root category

children = http_get(connection, '/t/products-cpg-nutrition')
pprint (children)


#pprint (children['ingredients'])

'''
for c in children['categories']:
    c_id = c['id']
    category = http_get(connection, '/fred/category/series', dict={"category_id": c_id})
    pprint (category)
    #category = http_get(connection, '')
    for s in category['seriess']:
        series = s['id']
        meta = http_get(connection, '/fred/series', dict={"series_id": series})
        
        
 # get the series in the given category

 # note: some category may not have any series
'''
