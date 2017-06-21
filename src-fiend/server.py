# File created by Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of Linode APP for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017

# from __future__ import print_function
#from uwsgidecorators import *

from flask import Flask, render_template, request
import requests # WILL ALLOW US TO POST TO THE PI
from fiend import Fiend # Personal module
import jinja2


global app
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

# JINJA PREP - loads template root paths, prepares environment
templateLoader = jinja2.FileSystemLoader( searchpath="/templates" )
templateEnv = jinja2.Environment( loader=templateLoader )

## FIEND FRAMEWORK INITIALIZER ##
@app.before_first_request
def initialize():
    global repo
    repo = Fiend()
    print("*** SERVER RUNNING, WAITING ON POST REQUEST ***\n")

# Include "no-cache" header in all POST responses
@app.after_request
def add_no_cache(response):
    if request.method == 'POST':
        response.cache_control.no_cache = True
    return response

## HOMEPAGE API ##    
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])	# Got em bleeding into each other - should work?
def serve():
#    vizvars = repo.get_dict() # Gets current incarnation of DB in dict-format
#    TEMPLATE_FILE = "/dataviz.html"
#    template = templateEnv.get_template( TEMPLATE_FILE )
#    return template.render(vizvars)
     return render_template('/dataviz.html')

## SMS API - PASSES TO PI ##
@app.route('/sms', methods=['POST'])
def parse_sms():
    message = str(request.form['Body']).strip().lower() # NOTE - Fiend object handles most input validation in-module
    sender = repo.get_hashable(str(request.form['From']))
    if (repo.new_entry({'name':sender,'msg':message})): # Also generates date/time specs with new_entry
    	data = repo.parse_command(message)
    package = convert_to_str(data)
    response = requests.post('http://127.0.0.1:54321/colors',data={'raw': package}) # Passes dict as FORM-ENCODED object to pi
    return "POSTED"

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=12345, debug=True)
