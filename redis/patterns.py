#!/usr/bin/python

import redis
import shutil
import chardet
from BeautifulSoup import BeautifulSoup
import re

redis = redis.Redis(host='localhost', port=6379, db=0)
limit = 1
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
    x = []
    y = []
    
    # HTMLDELIM = ["</title>", "</div>", "</script>", "</p>", "</li>", "</html>"]
    html = re.sub(r'<\/script>', "</script>\n", html)
    html = re.sub(r'<meta ', "\n<meta ", html)
    html = re.sub(r'<\/title>', "</title>\n", html)
    html = re.sub(r'<\/div>', "</div>\n", html)
    html = re.sub(r'<\/p>', "</p>\n", html)
    html = re.sub(r'<\/li>', "</li>\n", html)
    html = re.sub(r'<\/style>', "</style>\n", html)
    html = re.sub(r'<\/dd>', "</dd>\n", html)

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
                visiblecontent = soup.getText()
                for child in soup.recursiveChildGenerator():
                    name = getattr(child, "name", None)
                    if name is not None:
                         htmltags.append(name)
                    elif not child.isspace(): # leaf node, don't print spaces
                         donothing = 1
                matrix = {}
                visiblewords = len(visiblecontent.split())
                matrix['words'] = str(words)
                matrix['visiblewords'] = 0
                matrix['comas'] = comas
                matrix['dots'] = dots
                matrix['equal'] = equal
                matrix['html'] = line
                matrix['tags'] = str(visiblecontent)
                code = 'W' + str(visiblewords) + ',C' + str(comas) + ',D' + str(dots) + ',E' + str(equal)
                matrix['code'] = code
                if visiblewords > 10:
                    matrix['visiblewords'] = str(visiblewords)
                doc[lineID] = matrix
            lineID = lineID + 1    
        
    if debug:
        sorted(doc, key=int)
         
        #for lineID in doc:
        for lineID,item in doc.items():
        #lineID = 1003
            if lineID:
                code = item['code']
                line = str(item['html'])
                words = item['words']
                words = item['visiblewords']
                tags = item['tags']
                x.append(lineID)
                y.append(int(words))
                #print 'W' + str(words) + ' ' + line + ' ' + code
                if words:
                    print str(lineID) + ',' + code + ',' + line + '\t' + tags
    
    return (x,y,doc)

