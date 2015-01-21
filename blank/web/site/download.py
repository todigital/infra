#!/usr/bin/env python

import urllib
import re
import sys
import redis
from tld import get_tld
redis = redis.Redis(host='localhost', port=6379, db=0)
url = sys.argv[1]

def download(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def geturls(page, root):
    links = re.findall(r'href=[\'"]?([^\'" >]+)', page)
    urls = {}
    for url in links:
        regexp = r'news\\S+'
        match = re.match(r'\/news\S+', url)
        if match:
            fullurl = root + url
            urls[fullurl] = url
    return urls

if url:
    page = download(url)
    root = "http://" + get_tld(url)
    urls = geturls(page, root)
    redis.set(url, page)
    for url in urls:
        html = download(url)
        redis.set(url, html)

