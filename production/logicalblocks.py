#!/usr/bin/python

import vincent
import shutil
import re

def getblocks(x,y,doc):
    # Init
    coords = {}
    index = 0
    position = 0

    try:
        for lineID,item in doc.items():
            line = str(item['html'])
            openignore = re.match(r'<style|<script', line)
            closeignore = re.match(r'<\/style|<\/script', line)
            #lineID = 1003
            if lineID:
                status = ''
                code = item['code']
                line = item['line']
                words = item['words']
                words = item['visiblewords']
                tags = item['tags']
                index = item['index']
                activeflag = item['active']
                if item['status']:
                    status = item['status']
                x.append(lineID)
                y.append(int(words))
                outstr = '"' + str(lineID) + '"' + ',' + code
                if activeflag:
                    coords[lineID] = activeflag

                if status == 'active':
                    #index = lineID - position
                    outstr = outstr + ',' + str(index)
                    position = lineID
                    contentstr = str(lineID) + ' ' + '[' + str(index) + '] ' + tags
                    originstr = str(lineID) + line
                    #content.write(contentstr + '\n')
                    #origin.write(originstr + '\n')
                    #dataset.write(outstr + '\n')
                else:
                    xcode = '0,0,0,0,0,0,0,0,0,0'
                    outstr = '"' + str(lineID) + '"' + ',' + xcode
                    #dataset.write(outstr + '\n')
    except:
	print "Error\n"

    return coords

def getdistance(freq, posindex, DEBUG):
    maxDistance = 0
    rank = {}

    try:
        for x in sorted(freq):
            y = freq[x]
            if y > 1:
                maxDistance = x
                out = '[' + str(x) + ':' + str(y) + '] ' + posindex[x]
                Rmatrix = posindex[x].split()
                if DEBUG == 'distance':
                    print out
                for id in Rmatrix:
                    rank[id] = x
    except:
	print "Warning: error\n";

    return maxDistance

