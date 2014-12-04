#!/usr/bin/python

from couchdb import *
s = Server('http://127.0.0.1:5984/')
print len(s)

#http://lethain.com/an-introduction-to-using-couchdb-with-django/
#s.create('users')
#s.create('docs')
print len(s)

#db = s.create('docs1')
db = s['docs1']
print len(db)
db.create({'type':'Document','title':'Document One','txt':"This is some text."})
print len(db)
from uuid import uuid4
doc = {'_id': uuid4().hex, 'type': 'person', 'name': 'John Doe'}
db.create(doc)
# http://segfault.in/2010/11/playing-with-python-and-couchdb/
for docid in db:
    eml = db.get(docid)
    try:
        print eml['title']
    except:
	print eml['type']
