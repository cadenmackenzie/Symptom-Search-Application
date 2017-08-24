#!/usr/bin/env python

from pprint import pprint

import json

import http.client, urllib.parse

class WikiClass:
    
    def http_get(connection, path, query={}, headers=None, body=None):

        #&titles=San_Francisco&prop=images&imlimit=20&format=json
        query['action'] = 'query'
        query['prop'] = 'revisions'
        query['titles'] = 'Malaria'
        query['rvprop'] = 'content'
        query['format'] = 'jsonfm'
 
        #query['pageid'] = '593703'
        connection.request('GET', path + '?' + urllib.parse.urlencode(query), headers=None, body=None)
        print ('yes')
        response = connection.getresponse()
        print (response.reason, response.status)
    
        if response.status == 200:
            data = response.read() #will be in bytes
            return data
            #return json.loads(data.decode('utf-8'))

        else:
            raise Exception("HTTP call failed: " + response.reason)

    url = 'en.wikipedia.org' #API

    connection = http.client.HTTPSConnection(url) #create connection


    # get the children of the root category

    children = http_get(connection, '/w/api.php', query={})
    pprint (children)

    for line in children['batchcomplete']:
        print (line)
        if 'cure' in line:
            print (line)
