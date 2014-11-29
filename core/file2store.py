#!/usr/bin/python

from pymongo import MongoClient
import sys

filename = sys.argv[1]
try:
    year = sys.argv[2]
except:
    year = 2014	
try:
    country = sys.argv[3]
except:
    country = 'NLD'

client = MongoClient()
db = client.crawler  # use a database called boundaries to store json
collection = db.web   # and inside that DB, a collection called web

f = open(filename)  # open a file
text = f.read()    # read the entire contents, should be UTF-8 text
f.close()

print text
