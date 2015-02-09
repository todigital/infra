#!/usr/bin/env python

import urllib
import re
import sys
import redis
from urlparse import urlparse

redis = redis.Redis(host='localhost', port=6379, db=0)

root = "http://www.pravda.com.ua"
key = "http://www.pravda.com.ua/news"
url = "http://www.pravda.com.ua/news/2015/01/16/7055345/"
url = "http://echo.msk.ru"
url = "http://www.pravda.com.ua"
url = "http://nos.nl"
#url = "http://nos.nl/artikel/2018265-drie-zwaarbewapende-mannen-aangehouden-in-a-dam.html"
url = "http://dw.de"

def download(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def geturls(page,url):
    parsed_uri = urlparse(url)
    root = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

    links = re.findall(r'href=[\'"]?([^\'" >]+)', page)
    urls = {}
    for url in links:
        regexp = r'news\\S+'
        match = re.match(r'\/news\S+', url)
	match = 1
        if match:
	    fullurl = root + url
            urls[fullurl] = url
    return urls

page = download(url)
urls = geturls(page,url)
redis.set(key, url)
redis.set(url, page)
for url in urls:
    try:
        html = download(url)
        urls = geturls(html,url)
        redis.set(url, html)
    except:
	print url
