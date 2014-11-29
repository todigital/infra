#!/usr/bin/python
import recognizer
import sys
from BeautifulSoup import BeautifulSoup

def text_processor(htmlstrings, idealmodel, debug):
    result = {}
    structure = []
    fulltext = []
    title = ''
    attributes = {}
    
    # find title
    soup = BeautifulSoup(str(htmlstrings))
    title = soup.title.string
    attributes['title'] = title
    attributes['meta:description'] = str(soup.findAll(attrs={"name":"description"}))
    attributes['meta:keywords'] = str(soup.findAll(attrs={"name":"keywords"}))
    attributes['meta:author'] = str(soup.findAll(attrs={"name":"property"}))

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
                for child in soup.recursiveChildGenerator():
                    name = getattr(child, "name", None)
                    if name is not None:
                         htmltags.append(name)
                    elif not child.isspace(): # leaf node, don't print spaces
                         donothing = 1
                code = 'W' + str(words) + ',C' + str(comas) + ',D' + str(dots) + ',E' + str(equal)
                result[code] = lineID
                
                if idealmodel:
                    if idealmodel.has_key(code):
                        # ignore
                        fulltext.append('')
                    else:
                        true = 0
                        if words:
                            true = 1 
                        if 'a' in htmltags:
                            true = 0
                            
                        if true:
                            fulltext.append(line)
                        else:
                            fulltext.append('')
                
                # Save structure line by line
                stats = {}
                stats['lineID'] = lineID
                stats['code'] = code
                stats['words'] = words
                stats['comas'] = comas
                stats['dots'] = dots
                stats['equal'] = equal
                structure.append(stats)
                
                #print code
                if debug:
                    print 'STATS' + str(htmltags) + ' ' + '[' + code + '] '
                    print 'TXT' + ' ' + line
            lineID = lineID + 1
    return (result, structure, fulltext, attributes)
