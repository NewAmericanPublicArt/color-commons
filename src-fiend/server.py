# File created by Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of Linode app for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017

import datetime
from fiend import Fiend # Personal module
from flask import Flask, render_template, request
import json
from os import path
import requests # WILL ALLOW US TO POST TO THE PI
import time # separate module for calendar

global public
public = Flask(__name__, static_url_path="", static_folder="templates")
public.config['PROPAGATE_EXCEPTIONS'] = True

## FIEND FRAMEWORK INITIALIZER ##
@public.before_first_request
def initialize():
    global repo
    repo = Fiend()
    print("*** SERVER RUNNING, WAITING ON POST REQUEST ***")

## POST RESPONSE INITIALIZER; adds "no-cache" header ##
@public.after_request
def add_no_cache(response):
    if request.method == 'POST':
        response.cache_control.no_cache = True
    return response
  
## HOMEPAGE API ##    
@public.route('/', methods=['GET']) # Bleeding == nested functionality
@public.route('/index', methods=['GET'])	
def serve():
    print("@@@@@@@@@@@@@@@@@@@@@@@@serving repo "+str(repo.get_log())[:100])
    std = repo.load('current.csv') # CALLS JSDT AND HIERARCHY 1 AFTER THE OTHER
#    try:
    return render_template('/index.html',data=std,time=(repo.get_ms(repo.get_date(),repo.get_time())))
#    except:
#	return render_template('/except.html')

## SMS API; passes formatted input to pi ##
@public.route('/sms', methods=['POST'])
def parse_sms():
    message = str(request.form['Body']).strip().lower() # NOTE - Fiend object handles most input validation in-module
    sender = repo.get_hashable(str(request.form['From']))
    if (repo.new_entry({'name':sender,'msg':message})): # Also generates date/time specs with new_entry
    	data = repo.parse_command(message)
    package = repo.convert_to_str(data)
    response = requests.post('http://127.0.0.1:54321/colors',data={'raw': package}) # Passes dict as FORM-ENCODED object to pi
    return "POSTED"

# FILTER which finds & replaces all DT instances for js
@public.template_filter('strip_dt')
def strip_dt(hier):
   hier = repo.rm_dt(hier)
   return json.dumps(hier)

if __name__ == "__main__":
   public.run(host='0.0.0.0', port=12345, debug=True)
