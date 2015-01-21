#!/usr/bin/python
#%matplotlib inline

import redis
import vincent
vincent.core.initialize_notebook()
import shutil
import chardet
#from recognizer import text_processor, text_processor_test
from BeautifulSoup import BeautifulSoup
import re

redis = redis.Redis(host='localhost', port=6379, db=0)
limit = 2
count = 0
idealmodel = ''
debug = 0

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
        
    if debug:
        sorted(doc, key=int)
        
        #for lineID in doc:
        for lineID,item in doc.items():
            line = str(item['html'])
            openignore = re.match(r'<style|<script', line)
            closeignore = re.match(r'<\/style|<\/script', line)
        #lineID = 1003
            if lineID:
                code = item['code']
                words = item['words']
                words = item['visiblewords']
                tags = item['tags']
                status = item['status']
                x.append(lineID)
                y.append(int(words))
                if status == 'active':
                    outstr = str(lineID) + ',' + code + ',' + line + '\t' + tags                    
                    #print outstr + '\n'
                    f.write(outstr + '\n') # python will convert \n to os.linesep

    return (x,y,doc)

id = 0
keys = redis.keys('*');
for key in keys:
    id = id + 1
    filename = "./content/news.txt" + str(id)
    f = open(filename,'w')
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

        (x, y, pattern) = buildpattern(data, 'd')
        #x = [71,72,73,74]
        #y = [1, 1534, 0, 345]
        print x
        print y
        #bar = vincent.Bar(y)
        #bar.display()
        
        #(htmltest, structure, fulltext, attr) = text_processor(data, idealmodel, debug)
    count = count + 1
    f.close() # you can omit in most cases as the destructor will call if 
