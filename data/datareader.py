#!/usr/bin/python

import sys
import json
import simplejson
filename = "nlgeo.json.1"
filename = "nlgeo.json"

with open(filename) as json_file:
    json_data = json.load(json_file)
    loc = json_data['locations']

    cities = {}
    for cityline in loc:
	year = cityline['year']
	cityname = cityline['naam']
	if cities.has_key(cityname):
	    cities[cityname] = int(cities[cityname]) + 1 
	else:
	    print str(year) + ',' + cityline['amsterdam_code'] + ',' + str(cityline['naam'])
	    cities[cityname] = 1
