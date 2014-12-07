#!/usr/bin/python

from couchdb import *
s = Server('http://127.0.0.1:5984/')

database = 'nltest'
db = s[database]

for docid in db:
    item = db.get(docid)
    try:
        print item['url']
    except:
	print item['url']
