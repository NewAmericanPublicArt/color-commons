# File created by Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of Linode APP for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017
# from __future__ import print_function
#from uwsgidecorators import *
#import webcolors

from flask import Flask, render_template, request
import requests # WILL ALLOW US TO POST TO THE PI
from xkcd_colors import xkcd_names_to_hex # Special thanks!
from random import randint
import socket
from math import sin
import itertools
import array
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
    return render_template('/data.html')

## SMS API - PASSES TO PI ##
@app.route('/sms', methods=['POST'])
def parse_sms(): 
    message = str(request.form['Body']).strip().lower() # NOTE - Fiend object handles most input validation in-module
    sender = repo.get_hashable(str(request.form['from_']))
    if (repo.new_entry({'name':sender,'msg':message})): # Also generates date/time specs with new_entry
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
    package = convert_to_str(data)
    print(package) # TAKE OUT eventually
    response = requests.post('http://127.0.0.1:54321/colors', data={'raw':package})
    print(response)# TAKE OUT eventually

def complement(color): # pass color as (r, g, b) tuple
    # simpler, slower version of http://stackoverflow.com/a/40234924
    return tuple(max(color) + min(color) - channel for channel in color)

def look_up_color(name):
    try:
        color = webcolors.hex_to_rgb(xkcd_names_to_hex[name])
    except: # if we can't find a color, make up a random one
        color = [randint(0, 255), randint(0, 255), randint(0, 255)]
    return color

#def bitpack(arr):
#    condensed = bytearray(72) # Max RGB = 1byte*3 colors*2 lights*12 blades	
#    for i, x in enumerate(arr):
#	condensed += (x << (8*i)) # Packs in BIG ENDIAN FORMAT
#    return condensed

def convert_to_str(arr):
    condensed = ""
    for i, x in enumerate(arr):
	condensed+=str(x)
	if (i % 3 == 2):
	    condensed+="|"
	elif (i !=(len(arr)-1)):
            condensed += ","
	# Else, add nothing - last values
    return condensed

if __name__ == "__main__":
   app.run(host='127.0.0.1:5000', debug=True)
