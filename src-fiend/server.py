# File created by Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of Linode app for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017

import datetime
from fiend import Fiend # Personal module
from flask import Flask, json, render_template, request
from os import path
import requests # WILL ALLOW US TO POST TO THE PI
import time # separate module for calendar

global public
public = Flask(__name__, static_url_path="", static_folder="templates")
public.config['PROPAGATE_EXCEPTIONS'] = True
public.config['JSON_SORT_KEYS'] = False

## FIEND FRAMEWORK INITIALIZER ##
@public.before_first_request
def initialize():
    global repo
    repo = Fiend([],None)
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
    std = json.dumps(repo.defaultload('current.csv')) # rets a copy to ONLY log item of fiend/repo
    try:
        return render_template('/index.html',data=std,all=len(repo.get_log()),time=(repo.get_ms(repo.get_date(),repo.get_time())))
    except:
	   return render_template('/except.html')

## SMS API; passes formatted input to pi ##
@public.route('/sms', methods=['POST'])
def parse_sms():
    message = str(request.form['Body']).strip().lower() # NOTE - Fiend object handles most input validation in-module
    sender = str(request.form['From'])
    if (repo.new_entry({'name':sender,'msg':message})): # Also generates date/time specs with new_entry
    	data = repo.parse_command(message)
    package = repo.convert_to_str(data)
    response = requests.post('http://127.0.0.1:54321/colors',data={'raw': package}) # Passes dict as FORM-ENCODED object to pi
    return "POSTED"

@public.route('/serve', methods=['GET'])
def send_to_json():
    data = repo.thu_load('current.csv') # rets a copy to ONLY log item of fiend
    response = public.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response #https://stackoverflow.com/a/26961568

if __name__ == "__main__":
   public.run(host='0.0.0.0', port=12345, debug=True)
