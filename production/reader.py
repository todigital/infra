#!/usr/bin/python

import redis
import pickle
import shutil
import chardet
from BeautifulSoup import BeautifulSoup
import re
import operator
# content analysis packages
import logicalblocks
from patterns import buildpattern
from logicalblocks import getblocks
from logicalblocks import getdistance
from clusters import makeclusters 

redis = redis.Redis(host='localhost', port=6379, db=0)

# DEBUG levels
# extractor 
# distance
# cluster 
# generic
DEBUG = 'clusters'
#DEBUG = 'distance'

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
	    maxDistance = getdistance(freq, posindex, DEBUG)
	    if DEBUG == 'distance':
	        print '[Distance] ' + str(maxDistance)

	    clusterRank = makeclusters(maxDistance, doc, mainindex, DEBUG)
            x = clusterRank
            sorted_clusters = {k[0]:k[1] for k in sorted(x.items(), key=operator.itemgetter(0))}

	    if DEBUG == 'clusters':
		print sorted_clusters

	except:
	    skip = id

	print key
