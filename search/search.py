#!/usr/bin/python
from sphinxapi import SphinxClient

def search(q, index):
    if q:
        query = q
        s = SphinxClient()
        s.SetServer('127.0.0.1', 9312)
        s.SetLimits(0, 16777215)
	print s.Status()
        if s.Status():
            query_results = s.Query(query)
	    print query_results
	    #pages_id = [page['id'] for page in query_results['matches']]
            #total = query_results['total']
	    #print total

index = "monitorixnl"
search('and', index)
