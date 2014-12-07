#!/usr/bin/python

from couchdb import *
from uuid import uuid4
import sys
import re
import getopt
import os

filename = ''
folder = ''

s = Server('http://127.0.0.1:5984/')
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

database = 'testnl'
try:
    db = s.create(database)
except:
    db = s[database]

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
        # build a document to be inserted
	text_file_doc = {"_id": uuid4().hex, "year": year, "country": country, "file_name": filename, "json" : text, "url": url }
	db.create(text_file_doc)
