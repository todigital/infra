#!/usr/bin/python

import redis
redis = redis.Redis(host='localhost', port=6379, db=0)

keys = redis.keys('*');
for key in keys:
    type = redis.type(key);
    value = ''
    if type == 'string':
        val = redis.get(key);
        value = val
    if type == 'KV':
        val = redis.get(key);
	value = val
    if type == 'HASH':
        vals = redis.hgetall(key);
	value = vals
    if type == 'ZSET':
        vals = redis.zrange(key, 0, -1);
	value = vals
    print key
    print value

#file = argv[1]

#with open(file) as f:
#    filehtml = f.read()

#rs.set(file, filehtml)
