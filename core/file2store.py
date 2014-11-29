#!/usr/bin/python

from pymongo import MongoClient
import sys
import re

url = ''
files = []
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

files.append(filename)

for filename in files:
    with open(filename, 'r') as f:
        filetext = f.readlines()
    url = ''
    match = re.search('Monitorix-url: (\S+)', filetext[0])
    url = match.group(1)

    text = str(filetext)

    if url:
	print url
        # build a document to be inserted
        text_file_doc = {"year": year, "country": country, "file_name": filename, "json" : text }
        collection.insert(text_file_doc)

