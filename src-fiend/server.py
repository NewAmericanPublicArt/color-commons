# File created by Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of Linode app for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017

from flask import Flask, render_template, request
import requests # WILL ALLOW US TO POST TO THE PI
from fiend import Fiend # Personal module
from os import path
import datetime
import time

global public
public = Flask(__name__, static_url_path="", static_folder="templates")
public.config['PROPAGATE_EXCEPTIONS'] = True

## FIEND FRAMEWORK INITIALIZER ##
@public.before_first_request
def initialize():
    global repo
    repo = Fiend()
    print("*** SERVER RUNNING, WAITING ON POST REQUEST ***")

## Include "no-cache" header in all POST responses
@public.after_request
def add_no_cache(response):
    if request.method == 'POST':
        response.cache_control.no_cache = True
    return response

# FILTER which finds & replaces all DT instances for js
#@public.template_filter('format_dt')
#def PASS FUNCTION - not the converter but could call it
# and then essentially make a new field to propagate to js?

## HOMEPAGE API ##    
@public.route('/', methods=['GET'])
@public.route('/index', methods=['GET'])	# Got em bleeding into each other - should work?
def serve():
    repo.get_fr_csv('current.csv')
    std = repo.load()
    print("called load; why no render")
    print(type(std))
    print(repo.get_time())
    try:
        return render_template('/index.html',data=std,time=repo.get_time())
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
