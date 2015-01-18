#!/usr/bin/python

import redis
import shutil
import chardet

redis = redis.Redis(host='localhost', port=6379, db=0)
limit = 30
count = 0

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

        print data
    count = count + 1
