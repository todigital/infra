#!/usr/bin/python
import redis
import shutil
import chardet
import re
from recognizer import text_processor, text_processor_test
from BeautifulSoup import BeautifulSoup

redis = redis.Redis(host='localhost', port=6379, db=0)
limit = 20
count = 0
idealmodel = ''
debug = 0

def buildpattern(html, debug):
    doc = {}
    docwords = {}
    structure = []
    fulltext = []
    title = ''
    attributes = {}
    
    # HTMLDELIM = ["</title>", "</div>", "</script>", "</p>", "</li>", "</html>"]
    html = re.sub(r'<\/script>', "</script>\n", html)
    html = re.sub(r'<meta ', "\n<meta ", html)
    html = re.sub(r'<\/title>', "</title>\n", html)
    html = re.sub(r'<\/div>', "</div>\n", html)
    html = re.sub(r'<\/p>', "</p>\n", html)
    html = re.sub(r'<\/li>', "</li>\n", html)

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
                matrix = {}
                matrix['words'] = words
                matrix['comas'] = comas
                matrix['dots'] = dots
                matrix['equal'] = equal
                matrix['html'] = line
                code = 'W' + str(words) + ',C' + str(comas) + ',D' + str(dots) + ',E' + str(equal)
                matrix['code'] = code
                doc[lineID] = matrix
                lineID = lineID + 1  

    if debug:
	sorted(doc, key=int)
	for lineID in doc:
            item = doc[lineID]
            code = item['code']
            line = item['html']
            print str(lineID) + ',' + code + '		' + line
    
    return doc

keys = redis.keys('*');
for key in keys:
    type = redis.type(key);
    value = ''
    if type == 'string':
        val = redis.get(key);
        html = val

    if count <= limit:
        print 'URL ' + key
        result = chardet.detect(html)
        charset = result['encoding']
        if charset == 'utf-8':
            data = html
        else:
            data = html.decode(charset)

        pattern = buildpattern(data, '1')
        #(htmltest, structure, fulltext, attr) = text_processor(data, idealmodel, debug)
    count = count + 1
