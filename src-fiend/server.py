# File created by Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of Linode APP for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017

from __future__ import print_function
from flask import Flask, render_template, request
import requests # WILL ALLOW US TO POST TO THE PI
#from uwsgidecorators import *
from xkcd_colors import xkcd_names_to_hex # Special thanks!
#import webcolors
import time
from random import randint

import socket
#from ola.ClientWrapper import ClientWrapper
import array
from math import sin
import itertools
import sys
from fiend import Fiend # Personal module

global app
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

## FIEND FRAMEWORK INITIALIZER ##
@app.before_first_request
def initialize():
    global repo
    repo = Fiend()
    print("init'ed empty fiend")

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
    return render_template('/data.html')

## SMS API - PASSES TO PI ##
@app.route('/sms', methods=['POST'])
def parse_sms():
    message = str(request.form['Body']).strip().lower()
    sender = str(request.form['from_'])
    print(message+' '+sender)

    # NOW - throw to fiend object
    elem = {'name':'bevvy','msg':message,'stamp':'timegoeshere'}
    if (repo.new_entry(elem)):
    	universe = 1
    	num_fixtures = 24
    	data = array.array('B')
    	if(message == "secret"):
	    data.append(0)
            data.append(0)
            data.append(255)
            data.append(255)
            data.append(0)
            data.append(0)
            data = data * (num_fixtures/2)
        elif(message == "flip white"):
            data.append(255)
            data.append(255)
            data.append(255)
            data.append(0)
            data.append(0)
            data.append(0)
            data = data * (num_fixtures/2)
        elif(message == "flip black"):
            data.append(0)
            data.append(0)
            data.append(0)
            data.append(255)
            data.append(255)
            data.append(255)
            data = data * (num_fixtures/2)
        elif(message == "rainbow"):         # ASK ABOUT THIS
            rainbow_tuples = [(int(128 + 128 * sin(phase)), \
                int(128 + 128 * sin(2.094 + phase)), \
                int(128 + 128 * sin(4.189 + phase))) \
                for phase in [x/1000.0 for x in range(0, 6282, 6282/24)]]
            data = array.array('B', itertools.chain.from_iterable(rainbow_tuples))
        elif(message.startswith("flip")):
            remainder = message[4:].strip() # chop off flip and strip any spaces
            print(remainder)
            color = look_up_color(remainder)
            inverse = complement(color)
            print(color)
            print(inverse)
            data.append(color[0])
            data.append(color[1])
            data.append(color[2])
            data.append(inverse[0])
            data.append(inverse[1])
            data.append(inverse[2])
            data = data * (num_fixtures/2)
        else:
            color = look_up_color(message)
            data.append(color[0])
            data.append(color[1])
            data.append(color[2])
            data = data * num_fixtures

    # So now data has what we need - need to make a request to the raspbi
    response = requests.post('http://172.16.11.50/colors', data=data) #MIGHT NEED PORT INFO
    print('Reply:'+response)

def complement(color): # pass color as (r, g, b) tuple
    # simpler, slower version of http://stackoverflow.com/a/40234924
    return tuple(max(color) + min(color) - channel for channel in color)

def look_up_color(name):
    try:
        color = webcolors.hex_to_rgb(xkcd_names_to_hex[name])
    except: # if we can't find a color, make up a random one
        color = [randint(0, 255), randint(0, 255), randint(0, 255)]
    return color

if __name__ == "__main__":
   app.run(host='127.0.0.1:5000', debug=True)
