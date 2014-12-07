#!/usr/bin/python

from couchdb import *
import re
import sys
s = Server('http://127.0.0.1:5984/')

# default database
database = 'nltest'
day = sys.argv[1]
if day:
    #nl_20141203
    database = "nl_" + day
db = s[database]

print "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
print "<sphinx:docset xmlns:sphinx=\"http://sphinxsearch.com/\">"
print "	<sphinx:schema>"
print "	<sphinx:attr name=\"id\" type=\"int\"/>"
print "	<sphinx:field name=\"country\" attr=\"string\" />"
print "	<sphinx:field name=\"url\" attr=\"string\" />"
print "	<sphinx:attr name=\"year\" type=\"string\"/>"
print " <sphinx:attr name=\"file_name\" type=\"string\"/>"
print " <sphinx:attr name=\"json\" type=\"string\"/>"
print " <sphinx:attr name=\"content\" type=\"string\"/>"
print " <sphinx:attr name=\"_id\" type=\"string\"/>"
print "	</sphinx:schema>"

id = 0
# Create XML
for docid in db:
    item = db.get(docid)
    id = id + 1
    print "	<sphinx:document id=\"" + str(id) + "\">"
    for field in item:
	showline = 1
	if field == '_id1':
	    showline = 0
	if field == 'json1':
	    showline = 0
	if field == '_rev':
            showline = 0

	if showline:
	    thisfield = field
	    replaced = item[field]
	    removehtml = ''
	    if thisfield == 'json':
		removehtml = 1
	    if thisfield == 'content':
		removehtml = 1

	    if removehtml:
		s = item[field]
	        replaced = re.sub('<', '&lt;', s)
		replaced = re.sub('>', '&gt;', replaced)
		replaced = re.sub('&', '&amp;', replaced)
		if replaced:
	 	    item[field] = replaced
	    if thisfield == 'url':
		s = item[field]
	        replaced = re.sub('&', '&amp;', replaced)
		if replaced:
                    item[field] = replaced
            print "	<" + field + '>' + item[field] + "</" + field + ">"
    print "	</sphinx:document>"
print "</sphinx:docset>"
