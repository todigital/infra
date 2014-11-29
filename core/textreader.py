#!/usr/bin/python

import sys
from BeautifulSoup import BeautifulSoup
filename1 = sys.argv[1]
filename2 = sys.argv[2]

f = open(filename1)  # open a file
text = f.read()    # read the entire contents, should be UTF-8 text
f.close()

import urllib2
from BeautifulSoup import BeautifulSoup

def text_processor(filename, idealmodel, debug):
    result = {}
    structure = []
    fulltext = []
    soup = BeautifulSoup(text)
    
    with open(filename) as fp:
        lineID = 0
        for line in fp:
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
                result[code] = lineID
                
                if idealmodel:
                    if idealmodel.has_key(code):
                        # ignore
                        fulltext.append('')
                    else:
                        true = 0
                        if words:
                            true = 1 
                        if 'a' in htmltags:
                            true = 0
                            
                        if true:
                            fulltext.append(str(lineID) + ' ' + str(htmltags) + ' ' + code + ' ' + line)
                        else:
                            fulltext.append('')
                
                # Save structure line by line
                stats = {}
                stats['lineID'] = lineID
                stats['code'] = code
                stats['words'] = words
                stats['comas'] = comas
                stats['dots'] = dots
                stats['equal'] = equal
                structure.append(stats)
                
                #print code
                if debug:
                    print 'STATS' + str(htmltags) + ' ' + '[' + code + '] '
                    print 'TXT' + ' ' + line
            lineID = lineID + 1
    return (result, structure, fulltext)
 
idealmodel = ''
debug = 0
(htmltest, structure, fulltext) = text_processor(filename1, idealmodel, debug)
(htmltest, structure, fulltext) = text_processor(filename2, htmltest, '')
for line in fulltext:
    if line:
        print line
