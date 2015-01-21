#!/usr/bin/python

from flask import Flask, render_template
from flask import g
from flask import Response, make_response, request, send_from_directory
from twisted.web import http
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required
import json
import urllib2
import glob
import csv
import sys
import psycopg2
import psycopg2.extras
import pprint
import getopt
import ConfigParser
import HTMLParser
from subprocess import Popen, PIPE, STDOUT
import simplejson
import re
import os
from werkzeug import secure_filename

app = Flask(__name__)

@app.route('/chart')
def presentation(settings=''):
    apiurl = "/site/static/data.tsv"
    resp = make_response(render_template('d3chart.html', apiurl=apiurl))
    return resp

@app.route('/demo')
def demo(settings=''):
    apiurl = "/site/static/data.tsv"
    email = request.args.get('email')
    url = request.args.get('url')
    html = 'Processing ' + url + '...'
    resp = make_response(render_template('demo.html', apiurl=apiurl, html=html))
    return resp

@app.route('/')
def start(settings=''):
    resp = make_response(render_template('index.html'))
    return resp

app.debug = True
if __name__ == '__main__':
    app.run()

