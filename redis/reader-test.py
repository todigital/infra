%matplotlib inline

import redis
import shutil
import chardet
from recognizer import text_processor, text_processor_test
from BeautifulSoup import BeautifulSoup
import re

redis = redis.Redis(host='localhost', port=6379, db=0)
limit = 1
count = 0
idealmodel = ''
debug = 0

def plothist(x,y):
    import matplotlib.pyplot as plt
    from numpy.random import normal

    width = 1
    plt.bar(x,y, width)
    #plt.step(x,10)
    #plt.hist(y, color='r', alpha=0.5, label='Uniform')
    plt.xticks(x)
    plt.title("News Histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()
    
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
    html = re.sub(r'<\/script>', "</script>\n", html)
    html = re.sub(r'<meta ', "\n<meta ", html)
    html = re.sub(r'<\/title>', "</title>\n", html)
    html = re.sub(r'<\/div>', "</div>\n", html)
    html = re.sub(r'<\/p>', "</p>\n", html)
    html = re.sub(r'<\/li>', "</li>\n", html)
    html = re.sub(r'<\/style>', "</style>\n", html)
    html = re.sub(r'<\/dd>', "</dd>\n", html)

    htmlstrings = html.splitlines()

    if htmlstrings:
        lineID = 0
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
                matrix['words'] = str(words)
                matrix['visiblewords'] = 0
                matrix['comas'] = comas
                matrix['dots'] = dots
                matrix['equal'] = equal
                matrix['html'] = line
                matrix['tags'] = str(visiblecontent)
                code = 'W' + str(visiblewords) + ',C' + str(comas) + ',D' + str(dots) + ',E' + str(equal)
                matrix['code'] = code
                if visiblewords > 10:
                    matrix['visiblewords'] = str(visiblewords)
                doc[lineID] = matrix
            lineID = lineID + 1    
        
    if debug:
        sorted(doc, key=int)
         
        #for lineID in doc:
        for lineID,item in doc.items():
        #lineID = 1003
            if lineID:
                code = item['code']
                line = str(item['html'])
                words = item['words']
                words = item['visiblewords']
                tags = item['tags']
                x.append(lineID)
                y.append(int(words))
                #print 'W' + str(words) + ' ' + line + ' ' + code
                if words:
                    print str(lineID) + ',' + code + ',' + line + '\t' + tags
    
    return (x,y,doc)

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

        (x, y, pattern) = buildpattern(data, 'd')
        #x = [71,72,73,74]
        #y = [1, 1534, 0, 345]
        print x
        print y
        plothist(x,y)
        
        #(htmltest, structure, fulltext, attr) = text_processor(data, idealmodel, debug)
    count = count + 1
    
