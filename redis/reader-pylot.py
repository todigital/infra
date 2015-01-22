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
limit = 102
count = 0
idealmodel = ''
debug = 0

id = 0
keys = redis.keys('*');
for key in keys:
    id = id + 1
    datasetfile = DATASETDIR + "/news.txt" + str(id)
    contentfile = CONTENTDIR + "/news.txt" + str(id)
    content = open(contentfile,'w')
    dataset = open(datasetfile,"w")
    type = redis.type(key);
    value = ''
    if type == 'string':
        val = redis.get(key);
        html = val

    if count <= limit:
        print key
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
                words = item['words']
                words = item['visiblewords']
                tags = item['tags']
		if item['status']:
                    status = item['status']
                x.append(lineID)
                y.append(int(words))
                if status == 'active':
                    outstr = str(lineID) + ',' + code 
		    #+ ',' + line + '\t' 
		    contentstr = str(lineID) + ' ' + tags
		    content.write(contentstr + '\n') 
                    dataset.write(outstr + '\n') # python will convert \n to os.linesep
        print x
        print y
        
    count = count + 1
    content.close()
    dataset.close()
