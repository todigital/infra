#!/usr/bin/python

import re

def makeclusters(maxDistance, doc, mainindex, DEBUG):
    previd = 0
    clusters = {}
    rowcluster = []
    clusterID = 0
    maxDistance = maxDistance / 2
    #maxDistance = 10
    clusterRank = {}

    if DEBUG == 'clusters':
	print "Clustering...\n"

    try:
        for id in mainindex:
            x = id

	    # Attributes
            item = doc[id]
            words = item['visiblewords']
            comas = item['comas']
            dots = item['dots']
            code = item['code']

            try:
                Distance = rank[id]
            except:
                Distance = maxDistance

            if words <= 5:
                Distance = -1
                if comas <= 1:
                    if dots <= 1:
                        Distance = -1

            if item['date']:
                if item['timeflag']:
                    Distance = -1

            delta = id - previd
	    if DEBUG == 'clusters':
                print '[' + str(id) + '] ' + str(delta) + ' ' + code + ' ' + str(Distance) + ' ' + str(words)

            if abs(delta) <= Distance:
                # Extend cluster
                try:
                    rowcluster = clusters[clusterID]
                except:
                    rowcluster = []
                    clusterRank[clusterID] = 0
                rowcluster.append(id)
                clusters[clusterID] = rowcluster
            else:
                # New cluster
                clusterID = clusterID + 1
                rowcluster = []
                rowcluster.append(id)
                clusters[clusterID] = rowcluster
                clusterRank[clusterID] = 0

            clusterRank[clusterID] = clusterRank[clusterID] + int(words)
            previd = id
    except:
	print "Warning: error in cluster...\n";

    return clusterRank
