#!/usr/bin/python

import redis
import shutil
import chardet
from BeautifulSoup import BeautifulSoup
import re
import operator
from patterns import buildpattern

redis = redis.Redis(host='localhost', port=6379, db=0)
DATASETDIR = 'datasets'
CONTENTDIR = 'content'
ORIGDIR = 'original'
NEWSDIR = 'news'
HEADLINE = "\"id\",\"words\",\"words1\",\"comas\",\"dots\",\"equal\",\"urls\",\"time\",\"date\",\"active\",\"index\""
limit = 1
count = 0
idealmodel = ''
debug = 0

id = 0
keys = redis.keys('*');
for key in keys:
    id = id + 1
    datasetfile = DATASETDIR + "/sample" + str(id) + ".txt"
    contentfile = CONTENTDIR + "/sample" + str(id) + ".txt"
    origfile = ORIGDIR + "/sample" + str(id) + ".txt"
    newsfile = NEWSDIR + "/sample" + str(id) + ".txt"
    content = open(contentfile,'w')
    dataset = open(datasetfile,"w")
    origin = open(origfile,"w")
    news = open(newsfile,"w")
    type = redis.type(key);
    value = ''
    if type == 'string':
        val = redis.get(key);
        html = val

    if count <= limit:
        print key
	content.write(key + '\n')
	dataset.write(HEADLINE + '\n')
        result = chardet.detect(html)
        charset = result['encoding']
        if charset == 'utf-8':
            data = html
        else:
            data = html.decode(charset)

        (x, y, doc, freq, posindex, mainindex) = buildpattern(data, 'd')
	sorted(doc, key=int)
	coords = {}
	index = 0
	position = 0
        for lineID,item in doc.items():
            line = str(item['html'])
            openignore = re.match(r'<style|<script', line)
            closeignore = re.match(r'<\/style|<\/script', line)
            #lineID = 1003
            if lineID:
		status = ''
                code = item['code']
		line = item['line']
                words = item['words']
                words = item['visiblewords']
                tags = item['tags']
		index = item['index']
		activeflag = item['active']
		if item['status']:
                    status = item['status']
                x.append(lineID)
                y.append(int(words))
		outstr = '"' + str(lineID) + '"' + ',' + code
		if activeflag:
		    coords[lineID] = activeflag

                if status == 'active':
		    #index = lineID - position
		    outstr = outstr + ',' + str(index)
		    position = lineID
		    contentstr = str(lineID) + ' ' + '[' + str(index) + '] ' + tags
		    originstr = str(lineID) + line 
		    content.write(contentstr + '\n') 
		    origin.write(originstr + '\n')
		    dataset.write(outstr + '\n')	
		else:
		    xcode = '0,0,0,0,0,0,0,0,0,0'
		    outstr = '"' + str(lineID) + '"' + ',' + xcode
		    dataset.write(outstr + '\n')
        #print x
        #print y
        
        count = count + 1
        content.close()
        dataset.close()
        origin.close()

        for lineID,item in doc.items():
	    itemcode = 'NN'
	    if item['active'] == '1':
	        itemcode = 'T'
	    if item['active']:
	        item = doc[lineID]
	        line = itemcode + ' ' + str(lineID) + '[' + str(item['index']) + '] ' + ' ' + item['html'] + '\n'
	        news.write(line)
        news.close()

	maxDistance = 0
	rank = {}
        for x in sorted(freq):
	    y = freq[x]
	    if y > 1:
		maxDistance = x
	        out = '[' + str(x) + ':' + str(y) + '] ' + posindex[x]
		Rmatrix = posindex[x].split()
	        print out
		for id in Rmatrix:
		    rank[id] = x
  
	# Clustering
	previd = 0
	clusters = {}
	rowcluster = []
	clusterID = 0
	maxDistance = maxDistance / 2
	clusterRank = {}
	for id in mainindex:
	    x = id
	    item = doc[id]
	    words = item['words']
	    try:
	        Distance = rank[id]
	    except:
		Distance = maxDistance
	    if id - previd <= Distance:
		# Extend cluster		   
		try:
		    rowcluster = clusters[clusterID]
		except:
		    rowcluster = []	
		    clusterRank[clusterID] = 0 
		rowcluster.append(id)
		clusters[clusterID] = rowcluster
	    else:
		# New cluster
		clusterID = clusterID + 1
		rowcluster = []
		rowcluster.append(id)
		clusters[clusterID] = rowcluster	
		clusterRank[clusterID] = 0

	    clusterRank[clusterID] = clusterRank[clusterID] + int(words)
	    previd = id
	print mainindex
	print str(maxDistance)
	
	#sortedRank = sorted((value,key) for (key,value) in clusterRank.items())
	x = clusterRank
	sorted_x = {k[0]:k[1] for k in sorted(x.items(), key=operator.itemgetter(0))}

	orderID = 0
	newstext = ''
	comments = []
	for clusterID, value in sorted(clusterRank.iteritems(), key=lambda (k,v): (v,k), reverse = True):
	    row = clusters[clusterID]
	    if orderID == 0:
                for id in row:
		    item = doc[id]
		    text = item['tags']
		    newstext = newstext + text + ' ' 
	    else:
		comments.append(row)
	    orderID = orderID + 1
	    #print '[' + str(clusterID) + ':' + str(clusterRank[clusterID]) + '] ' + str(row)

	print newstext
