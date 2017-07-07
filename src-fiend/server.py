# File created by Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of Linode app for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017

# from __future__ import print_function
#from uwsgidecorators import *

from flask import Flask, render_template, request
import requests # WILL ALLOW US TO POST TO THE PI
from fiend import Fiend # Personal module
# from jinja2 import FileSystemLoader, Environment
from os import path

global public
public = Flask(__name__)
public.config['PROPAGATE_EXCEPTIONS'] = True

## FIEND FRAMEWORK INITIALIZER ##
@public.before_first_request
def initialize():
    global repo
    repo = Fiend()
#   repo.tEnv = Environment( loader=FileSystemLoader('/templates',encoding='utf=8'),auto_reload=True )
    print("*** SERVER RUNNING, WAITING ON POST REQUEST ***\n")

## Include "no-cache" header in all POST responses
@public.after_request
def add_no_cache(response):
    if request.method == 'POST':
        response.cache_control.no_cache = True
    return response

## HOMEPAGE API ##    
@public.route('/', methods=['GET'])
@public.route('/index', methods=['GET'])	# Got em bleeding into each other - should work?
def serve():
#   PAGE = 'dataviz.html'
#   template = repo.tEnv.get_template(PAGE) 
    list = repo.get_log() # Gets current incarnation of DB in dict-format
    time = repo.get_time()
    try:
	return render_template('/dataviz.html',log=list,time=time)
    except:
	return render_template('/except.html')

## SMS API - PASSES TO PI ##
@public.route('/sms', methods=['POST'])
def parse_sms():
    message = str(request.form['Body']).strip().lower() # NOTE - Fiend object handles most input validation in-module
    sender = repo.get_hashable(str(request.form['From']))
    if (repo.new_entry({'name':sender,'msg':message})): # Also generates date/time specs with new_entry
    	data = repo.parse_command(message)
    package = repo.convert_to_str(data)
    response = requests.post('http://127.0.0.1:54321/colors',data={'raw': package}) # Passes dict as FORM-ENCODED object to pi
    return "POSTED"

if __name__ == "__main__":
   public.run(host='0.0.0.0', port=12345, debug=True)
