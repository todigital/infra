#!/usr/bin/env python

import urllib
import re
import sys
import redis
redis = redis.Redis(host='localhost', port=6379, db=0)

root = "http://www.pravda.com.ua"
key = "http://www.pravda.com.ua/news"
url = "http://www.pravda.com.ua/news/2015/01/16/7055345/"

def download(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def geturls(page):
    links = re.findall(r'href=[\'"]?([^\'" >]+)', page)
    urls = {}
    for url in links:
        regexp = r'news\\S+'
        match = re.match(r'\/news\S+', url)
        if match:
	    fullurl = root + url
            urls[fullurl] = url
    return urls

page = download(url)
urls = geturls(page)
redis.set(key, url)
redis.set(url, page)
for url in urls:
    html = download(url)
    #urls = geturls(page)
    redis.set(url, html)
