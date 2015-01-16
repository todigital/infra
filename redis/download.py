#!/usr/bin/env python
import urllib
import re
import sys
import redis
redis = redis.Redis(host='localhost', port=6379, db=0)

key = "http://www.pravda.com.ua/news"
url = "http://www.pravda.com.ua/news/2015/01/16/7055345/"

def download(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

page = download(url)
redis.set(key, url)
redis.set(url, page)
print page
