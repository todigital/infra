#!/usr/bin/python

import redis
redis = redis.Redis(host='localhost', port=6379, db=0)

keys = redis.keys('*');
for key in keys:
    type = redis.type(key);
    print key
    if type == 'KV':
        val = redis.get(key);
    if type == 'HASH':
        vals = redis.hgetall(key);
    if type == 'ZSET':
        vals = redis.zrange(key, 0, -1);
    print key

#file = argv[1]

#with open(file) as f:
#    filehtml = f.read()

#rs.set(file, filehtml)
