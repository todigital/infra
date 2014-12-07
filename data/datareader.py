#!/usr/bin/python

import sys
import json
import simplejson
filename = "nlgeo.json.1"

with open(filename) as json_file:
    json_data = json.load(json_file)
    loc = json_data['locations']

    for cityline in loc:
	print cityline
