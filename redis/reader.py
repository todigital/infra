#!/usr/bin/python
import redis
import shutil
import chardet
from recognizer import text_processor, text_processor_test
from BeautifulSoup import BeautifulSoup

redis = redis.Redis(host='localhost', port=6379, db=0)
limit = 2
count = 0
idealmodel = ''
debug = 0

def buildpattern(html, debug):
    result = {}
    structure = []
    fulltext = []
    title = ''
    attributes = {}
    
    htmlstrings = html.splitlines()
    if htmlstrings:
        lineID = 0
        for line in htmlstrings:
            lenstr = len(line)
            words = len(line.split())
            comas = len(line.split(","))
            dots = len(line.split("."))
            equal = len(line.split("="))
            soup = BeautifulSoup(line)
            if words:
                htmltags = []
                for child in soup.recursiveChildGenerator():
                    name = getattr(child, "name", None)
                    if name is not None:
                         htmltags.append(name)
                    elif not child.isspace(): # leaf node, don't print spaces
                         donothing = 1
                code = 'W' + str(words) + ',C' + str(comas) + ',D' + str(dots) + ',E' + str(equal)
                result[lineID] = code
		lineID = lineID + 1

    if debug:
	sorted(result, key=int)
	for lineID in result:
	    code = result[lineID]
            print str(lineID) + ',' + code
    
    return result

keys = redis.keys('*');
for key in keys:
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

        pattern = buildpattern(data, '1')
        #(htmltest, structure, fulltext, attr) = text_processor(data, idealmodel, debug)
    count = count + 1
