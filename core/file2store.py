#!/usr/bin/python

from couchdb import *
from uuid import uuid4
import codecs
import sys
import re
import getopt
import os
import chardet
import shutil

filename = ''
folder = ''

s = Server('http://127.0.0.1:5984/')
options, remainder = getopt.getopt(sys.argv[1:], 'o:vf:d:D:l:', ['filename=', 
							 'lang=',
                                                         'verbose',
                                                         'version=',
						 	 'directory='
							 'date='
                                                         ])
for opt, arg in options:
    if opt in ('-d', '--directory'):
        folder = arg
    if opt in ('-D', '--date'):
        date = arg
    if opt in ('-l', '--lang'):
	lang = arg
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

database = 'nl'
if lang:
    database = lang
if date:
    database = database + '_' + date
print database
try:
    db = s.create(database)
except:
    #s.delete(database)
    #db = s.create(database)
    db = s[database]

if filename:
    files.append(filename)
if folder:
    print folder 
    for f in os.listdir(folder):
	fullpath = folder + '/' + f
	files.append(fullpath)

for filename in files:
    url = ''
    text = '' 
    try:
	# Read/convert to utf-8
	f = open(filename, 'r').read()
        result = chardet.detect(f)
        charset = result['encoding']
        if charset == 'utf-8':
	    filetext = f
        else:
            filetext = f.decode(charset)
    	    fpath = os.path.abspath(filename)
    	    newfilename = fpath + '.orig'
    	    shutil.copy(filename, newfilename)
	    print newfilename
    	    f = open(filename, 'w')
            try:
                f.write(filetext)
            except Exception, e:
                print e
            finally:
                f.close()

        match = re.search('Monitorix-url: (\S+)', filetext)
        url = match.group(1)
	text = str(filetext)
    except:
	skip = 1

    if url:
        # build a document to be inserted
	text_file_doc = {"_id": uuid4().hex, "year": year, "country": country, "file_name": filename, "content" : text, "url": url }
	db.create(text_file_doc)
