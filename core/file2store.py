#!/usr/bin/python

from pymongo import MongoClient
import sys
import re
import getopt
import os

filename = ''
folder = ''
options, remainder = getopt.getopt(sys.argv[1:], 'o:vf:d:', ['filename=', 
                                                         'verbose',
                                                         'version=',
						 	 'directory='
                                                         ])
for opt, arg in options:
    if opt in ('-d', '--directory'):
        folder = arg
    if opt in ('-f', '--filename'):
        filename = arg
    elif opt in ('-v', '--verbose'):
        verbose = True
    elif opt == '--version':
        version = arg

url = ''
files = []
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

if filename:
    files.append(filename)
if folder:
    print folder 
    for f in os.listdir(folder):
	fullpath = folder + '/' + f
	files.append(fullpath)

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
	try:
            text_file_doc = {"year": year, "country": country, "file_name": filename, "json" : text }
            collection.insert(text_file_doc)
	except:
	    print "Can't insert " + url

