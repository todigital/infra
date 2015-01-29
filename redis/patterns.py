#!/usr/bin/python

import redis
import vincent
import shutil
import chardet
from BeautifulSoup import BeautifulSoup
import re

YEAR = 2015
def buildpattern(html, debug):
    doc = {}
    docwords = {}
    structure = []
    fulltext = []
    title = ''
    attributes = {}
    x = []
    y = []
    table = {}
    Rindex = {}
    Mindex = []
    
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
	go = 1
	position = 0
	index = 0
        for line in htmlstrings:
	    matrix = {}
            lenstr = len(line)
            words = len(line.split())
            comas = len(line.split(","))
            dots = len(line.split("."))
            equal = len(line.split("="))
            soup = BeautifulSoup(line)
            
            if go:
                htmltags = []
                visible = soup.getText()
		visiblecontent = visible
                for child in soup.recursiveChildGenerator():
                    name = getattr(child, "name", None)
                    if name is not None:
                         htmltags.append(name)
                    elif not child.isspace(): # leaf node, don't print spaces
                         donothing = 1
		time = '0'
		date = ''
		activeflag = 0
                visiblewords = len(visible.split())
                
                openignore = re.match(r'<style|<script', line)
                closeignore = re.match(r'<\/style|<\/script', line)
                urlstatus = re.findall(r'<a', line)
                timeflag = re.findall('([0-9]+:[0-9]+)', line)
		dateflag = re.findall(r'20\d{2}', line)
                if openignore:
                    active = 0 
                            
		matrix['line'] = line
                matrix['words'] = str(words)
                matrix['visiblewords'] = 0
                matrix['comas'] = comas
                matrix['dots'] = dots
                matrix['equal'] = equal
                matrix['html'] = line
                matrix['status'] = 'active'
		matrix['date'] = 0
		if dateflag:
		    matrix['date'] = dateflag[0]
		    activeflag = 1
                if timeflag:
		    activeflag = 1
                    matrix['timeflag'] = 1 
		    time = timeflag[0]
		    visiblecontent = re.sub(r'([0-9]+:[0-9]+)', r'\1 ', visiblecontent)
                else:
                    matrix['timeflag'] = 0
                matrix['tags'] = str(visiblecontent)
                if urlstatus:
                    matrix['urlstatus'] = 1
                else:
                    matrix['urlstatus'] = 0
                #code = 'W' + str(visiblewords) + ',C' + str(comas) + ',D' + str(dots) + ',E' + str(equal) + ',U' + str(matrix['urlstatus']) + 'T' + str(matrix['timeflag'])
                if visiblewords > 0:
                    activeflag = 2
                    matrix['visiblewords'] = str(visiblewords)

		matrix['active'] = activeflag
		code = str(visiblewords) + ',' + str(comas) + ',' + str(dots) + ',' + str(equal) + ',' + str(matrix['urlstatus']) + ',' + str(matrix['timeflag']) + ',' + time + ',' + str(matrix['date']) + ',' + str(activeflag)
                matrix['code'] = code

                if active == 0:
                    matrix['visiblewords'] = 0
                    matrix['status'] = 'ignored'
                if visiblewords <= 1:
                    matrix['status'] = 'ignored'

		if matrix['status'] == 'ignored':
		    code = '0,0,0,0,0,0,0,0,0,0'
		    matrix['active'] = 0
		    matrix['code'] = code
		    matrix['index'] = 0
		else:
		    index = lineID - position
		    matrix['index'] = index 
		    Mindex.append(lineID)
		    try: 
			table[index] = table[index] + 1
			Rindex[index] = Rindex[index] + str(lineID) + ' '
		    except:
			table[index] = 1
			Rindex[index] = str(lineID) + ' '
		    position = lineID

                if closeignore:
                    active = 1

	        doc[lineID] = matrix
            lineID = lineID + 1    
        
    for Windex in sorted(table):
        Wval = table[Windex]
        if Wval > 1:
            out = str(Windex) + ' ' + str(Wval)
            #print out
	#1 21
	#2 21
	#3 8

    return (x,y,doc,table,Rindex,Mindex)
