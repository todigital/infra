#!/usr/bin/python

import redis
import shutil
import chardet
from BeautifulSoup import BeautifulSoup
import re
from patterns import buildpattern

redis = redis.Redis(host='localhost', port=6379, db=0)
DATASETDIR = 'datasets'
CONTENTDIR = 'content'
ORIGDIR = 'original'
HEADLINE = "\"id\",\"words\",\"words1\",\"comas\",\"dots\",\"equal\",\"urls\",\"time\",\"date\""
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
    content = open(contentfile,'w')
    dataset = open(datasetfile,"w")
    origin = open(origfile,"w")
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

        (x, y, doc) = buildpattern(data, 'd')
	sorted(doc, key=int)
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
		if item['status']:
                    status = item['status']
                x.append(lineID)
                y.append(int(words))
		outstr = '"' + str(lineID) + '"' + ',' + code
                if status == 'active':
		    contentstr = str(lineID) + ' ' + tags
		    originstr = str(lineID) + line 
		    content.write(contentstr + '\n') 
		    origin.write(originstr + '\n')
		    dataset.write(outstr + '\n')	
		else:
		    xcode = '0,0,0,0,0,0,0,0'
		    outstr = '"' + str(lineID) + '"' + ',' + xcode
		    dataset.write(outstr + '\n')
        print x
        print y
        
    count = count + 1
    content.close()
    dataset.close()
    origin.close()
