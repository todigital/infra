#!/usr/bin/python

import redis
import vincent
import shutil
import chardet
from BeautifulSoup import BeautifulSoup
import re

def buildpattern(html, debug):
    doc = {}
    docwords = {}
    structure = []
    fulltext = []
    title = ''
    attributes = {}
    x = []
    y = []
    
    # HTMLDELIM = ["</title>", "</div>", "</script>", "</p>", "</li>", "</html>"]
    html = re.sub(r'<script', "\n<script", html)
    html = re.sub(r'<a', " <a", html)
    html = re.sub(r'<style', "\n<style", html)
    html = re.sub(r'<\/script>', "\n</script>\n", html)
    html = re.sub(r'<meta ', "\n<meta ", html)
    html = re.sub(r'<\/title>', "</title>\n", html)
    html = re.sub(r'<\/div>', "</div>\n", html)
    html = re.sub(r'<\/p>', "</p>\n", html)
    html = re.sub(r'<\/li>', "</li>\n", html)
    html = re.sub(r'<\/style>', "\n</style>\n", html)
    html = re.sub(r'<\/dd>', "</dd>\n", html)

    htmlstrings = html.splitlines()

    if htmlstrings:
        lineID = 0
        active = 1
        for line in htmlstrings:
            lenstr = len(line)
            words = len(line.split())
            comas = len(line.split(","))
            dots = len(line.split("."))
            equal = len(line.split("="))
            soup = BeautifulSoup(line)
            
            if words:
                htmltags = []
                visiblecontent = soup.getText()
                for child in soup.recursiveChildGenerator():
                    name = getattr(child, "name", None)
                    if name is not None:
                         htmltags.append(name)
                    elif not child.isspace(): # leaf node, don't print spaces
                         donothing = 1
                matrix = {}
                visiblewords = len(visiblecontent.split())
                
                openignore = re.match(r'<style|<script', line)
                closeignore = re.match(r'<\/style|<\/script', line)
                urlstatus = re.findall(r'<a', line)
                timeflag = re.findall('([0-9]+:[0-9]+)', line)
                if openignore:
                    active = 0 
                            
                matrix['words'] = str(words)
                matrix['visiblewords'] = 0
                matrix['comas'] = comas
                matrix['dots'] = dots
                matrix['equal'] = equal
                matrix['html'] = line
                matrix['status'] = 'active'
                if timeflag:
                    matrix['timeflag'] = str(timeflag)
                else:
                    matrix['timeflag'] = ''
                matrix['tags'] = str(visiblecontent)
                if urlstatus:
                    matrix['urlstatus'] = 1
                else:
                    matrix['urlstatus'] = 0
                code = 'W' + str(visiblewords) + ',C' + str(comas) + ',D' + str(dots) + ',E' + str(equal) + ',U' + str(matrix['urlstatus']) + 'T' + matrix['timeflag']
                matrix['code'] = code
                if visiblewords > 0:
                    matrix['visiblewords'] = str(visiblewords)
                if active == 0:
                    matrix['visiblewords'] = 0
                    matrix['status'] = 'ignored'
                if visiblewords <= 1:
                    matrix['status'] = 'ignored'
                doc[lineID] = matrix

                if closeignore:
                    active = 1

            lineID = lineID + 1    
        
    return (x,y,doc)
