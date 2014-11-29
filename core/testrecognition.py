#!/usr/bin/python

import sys
from recognizer import text_processor

from BeautifulSoup import BeautifulSoup
filename1 = sys.argv[1]
filename2 = sys.argv[2]

with open(filename1, 'r') as f:
    filetext1 = f.readlines()
with open(filename2, 'r') as f:
    filetext2 = f.readlines()

idealmodel = ''
debug = 0
(htmltest, structure, fulltext, attr) = text_processor(filetext1, idealmodel, debug)
(htmltest, structure, fulltext, attr) = text_processor(filetext2, htmltest, '')
for line in fulltext:
    if line:
        print line

print attr['title']
print attr['meta']
