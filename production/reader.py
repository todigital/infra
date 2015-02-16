#!/usr/bin/python

import redis
import pickle
import shutil
import chardet
from BeautifulSoup import BeautifulSoup
import re
import operator
import logicalblocks
from patterns import buildpattern
from logicalblocks import getblocks
from logicalblocks import getdistance

redis = redis.Redis(host='localhost', port=6379, db=0)

filter = "*2015/02/13/7058423*"
keys = redis.keys(filter)
id = 0
for key in keys:
    id = id + 1
    type = redis.type(key);

    value = ''
    if type == 'string':
        val = redis.get(key);
        html = val 

        result = chardet.detect(html)
        charset = result['encoding']
        if charset == 'utf-8':
            data = html
        else:
            data = html.decode(charset)

	try:
	    (x, y, doc, freq, posindex, mainindex) = buildpattern(data, 'd')
            sorted(doc, key=int)
	    structure = getblocks(x,y,doc)
	    maxdistance = getdistance(freq)
	    print maxdistance
	except:
	    skip = id

	print key
