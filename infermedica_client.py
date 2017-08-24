#!/usr/bin/env python

from pprint import pprint

import json

import http.client, urllib.parse
import urllib


def http_get(connection, method, path, header, body=None):
    
    connection.request(method, path, headers=header, body=body)
    response = connection.getresponse()
    #print (response.reason, response.status)
    if response.status == 200:
        data = response.read() #will be in bytes
        return json.loads(data.decode('utf-8'))
        #return data
    elif response.status == 404:
        return 'Your request does not match any results'
    else:
        raise Exception("HTTP call failed: " + response.reason)

def http_wiki_get(connection, method, path, header, body=None):
    
    connection.request(method, path, headers=header, body=body)
    response = connection.getresponse()
    #print (response.reason, response.status)
    if response.status == 200:
        data = response.read() #will be in bytes
        return data.decode('utf-8')
        #return json.loads(data.decode('utf-8'))
        #return data

    else:
        raise Exception("HTTP call failed: " + response.reason)

def http_factual_get(connection, path, ingredient):
    dict = {}
    dict['KEY'] = 'EE20JKBHtxwSIZrgLQvcntLC3CpUcOW5BYXT93Qu'
    dict['q'] = ingredient
    connection.request('GET', path + '?' + urllib.parse.urlencode(dict))
    response = connection.getresponse()

    if response.status == 200:
        data = response.read() #will be in bytes
        return json.loads(data.decode('utf-8'))
    else:
        raise Exception("HTTP call failed: " + response.reason)

def infermedica_lookup(query_search):
    header = {}
    body = {}
    header['app_id'] = '049731ed'
    header['app_key'] = 'a396db155587b40aa6a15f5752a1bc2a'
    header['Content-Type'] = 'application/json'
    header['Accept'] = 'application/json'
    method_get = 'GET'
    method_post = 'POST'
    url = 'api.infermedica.com'
    connection = http.client.HTTPSConnection(url) 
    query = '?phrase=' + query_search
    lookup = http_get(connection, method_get, '/v1/lookup' + query, header, body)
    if lookup == 'Your request does not match any results':
        return 'Your request does not match any results'
    else:
        return lookup['id']

def infermedica_diagnosis(symptom_id):
    header = {}
    body = {}
    header['app_id'] = '049731ed'
    header['app_key'] = 'a396db155587b40aa6a15f5752a1bc2a'
    header['Content-Type'] = 'application/json'
    header['Accept'] = 'application/json'
    method_get = 'GET'
    method_post = 'POST'
    url = 'api.infermedica.com'
    connection = http.client.HTTPSConnection(url) 
    body['age'] = 20
    body['sex'] = 'female'
    body['evidence'] = [{'id': symptom_id, 'choice_id': 'present'}]
    data = json.dumps(body)
    diagnosis = http_get(connection, method_post, '/v1/diagnosis', header, data)
    
    #pprint (diagnosis)
    items = diagnosis['conditions']
    diag_list = []
    counter = 0
    for line in items:
        if counter < 1:
            diag_list.append(line)
            counter = counter + 1
        else:
            break
    for item in diag_list:
        print (item['name'])
        print ("The probability of you having a " + item['name'] + " is " + str(item['probability']))
        answer = input("Would you like to search for a cure? (yes or no)")
        if answer == 'yes':
            return item['name']
        else:
            return 'no'

def wiki_search(symptom):
    header = {}
    body = {}
    url = 'en.wikipedia.org'
    connection = http.client.HTTPSConnection(url)
    query = {}
    query['action'] = 'query'
    query['prop'] = 'revisions'
    query['titles'] = symptom
    query['rvprop'] = 'content'
    query['format'] = 'json'
    url_query = urllib.parse.urlencode(query)
    path = '/w/api.php' + '?' + url_query
    search = http_wiki_get(connection, 'GET', path, header, body)
    healing_chemicals = ['streptomycin', 'sanamycin', 'seomycin', 'sentamycin', 'vancomycin', 'teicoplanin', 'ramoplanin',
                        'amoxicillin', 'ampicillin', 'azlocillin', 'carbenicillin', 'cloxacillin', 'dicloxacillin',
                        'flucloxacillin', 'mezlocillin', 'dafcillin', 'penicillin', 'demeclocycline', 'doxycycline',
                        'minocycline', 'oxytetracycline', 'tetracycline', 'acetaminophen', 'morphine', 'benzalkonium chloride',
                        'boric acid', 'hydrogen peroxide', 'iodine', 'phenol', 'sodium hypochlorite']
    cures_list =[]
    for item in healing_chemicals:
        if item in search:
            lookup = factual_search(item)
            if lookup not in cures_list:
                cures_list.append(lookup)
    pprint (cures_list)
    
def factual_search(ingredient):
    url = 'api.v3.factual.com' #API
    connection = http.client.HTTPSConnection(url) #create connection
    products = http_factual_get(connection, '/t/products-cpg-nutrition', ingredient)
    
    return products

def options():
    print ("Menu: ")
    print ("A - Lookup symptom")
    print ("Z - End program")
    letter = input ("Please choose an option from the menu above: ")
    return letter

letter = ''
while (letter == 'A' or 'B'  or ''):
    letter = options()
    if letter == "A":

        query_search = input ("Enter Symptoms: ")
        symptom_id = infermedica_lookup(query_search)
        if symptom_id == 'Your request does not match any results':
            print (symptom_id)
            break
        diag = infermedica_diagnosis(symptom_id)
        if diag == 'no':
            print ('Program Ended')
            break
        else:
            wiki = wiki_search(diag)
    elif letter == 'Z':
        print ('Program Ended')
        break
    else:
        print ("Your request is not valid")
        break








