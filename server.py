from __future__ import print_function
from flask import Flask, render_template, request
from uwsgidecorators import *
from xkcd_colors import xkcd_names_to_hex
import webcolors
import time
from random import randint

import socket
from ola.ClientWrapper import ClientWrapper
import array
import sys

wrapper = None

public = Flask(__name__)
public.config['PROPAGATE_EXCEPTIONS'] = True

# Include "no-cache" header in all POST responses
@public.after_request
def add_no_cache(response):
    if request.method == 'POST':
        response.cache_control.no_cache = True
    return response

### Home page ###
@public.route('/')
@public.route('/index.html')
def default_page():
    return render_template('/index.html')

def DmxSent(status):
  if status.Succeeded():
    print('Success!')
  else:
    print('Error: %s' % status.message, file=sys.stderr)

  global wrapper
  if wrapper:
    wrapper.Stop()

@public.route('/sms', methods=['POST'])
def parse_sms():
    message = str(request.form['Body']).strip().lower()
    print("Received text message: " + message)
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
    else:
        try:
            color = webcolors.hex_to_rgb(xkcd_names_to_hex[message])
        except:
            color = [randint(0, 255), randint(0, 255), randint(0, 255)]
        data.append(color[0])
        data.append(color[1])
        data.append(color[2])
        data = data * num_fixtures

    ip = "172.16.11.50"
    port = 5000
    message = "listentome"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (ip, port))

    time.sleep(0.1)
    global wrapper
    wrapper = ClientWrapper()
    client = wrapper.Client()
    client.SendDmx(universe, data, DmxSent)
    wrapper.Run()
    return ('<?xml version="1.0" encoding="UTF-8" ?><Response></Response>')

	# Rainbow across all blades
	# Simple. Everyone wants this and loves it. 
	# I like when the two lights on each blade are different creating a little variance across the blade itself. 



	# (this next one is the stretch goal. But represents a how new data set of user experimentation.)

	# Modifier  
	# Use the word 'secret' as a modifier. 
	# I've written in some code that will get you thinking, for better or worse.

	# Example text : 'secret turquoise'

	# Result : lights show turquoise and the inverse of turquoise, alternating between lights.
	# (the same way secret does red and blue alternating between lights)

	# How : 
	# 1. The code checks if the message begins with the word secret

	# 2. if 'secret' is only the word then just play the standard alternating color secret show.
	  
	# 3. if there is a word after 'secret' then try the second word in the data base

	# 4. use the new color hex in an inverse color function : Linked here (shown below)

	# 5. Alternate between lights with the two colors.


	# This is a great site that can show you what some of these inverses are : http://coloreminder.com/


	# Here's my quick cut and paste psudo code

	# # Sum of the min & max of (a, b, c) 
	# def hilo(a, b, c): 
	# if c < b: b, c = c, b 
	# if b < a: a, b = b, a 
	# if c < b: b, c = c, b 
	# return a + c 

	# def complement(r, g, b): 
	# k = hilo(r, g, b) 
	# return tuple(k - u for u in (r, g, b))

	# if(message.startswith("secret")):
	# if len(message.split()) > 1:
	# try:
	# color = webcolors.hex_to_rgb(xkcd_names_to_hex[message.split(" ")[1]])
	# except:
	# color = [randint(0, 255), randint(0, 255), randint(0, 255)]

	# # this part is above my pay grade. Need a var colorInverse with new rgb values in it's array.
	# # need to use the above complement function, but don't know how

	# data.append(color[0])
	# data.append(color[1])
	# data.append(color[2])
	# data.append(colorInverse[0])
	# data.append(colorInverse[1])
	# data.append(colorInverse[2])
	# data = data * (num_fixtures/2)

	# else
	# data.append(0)
	# data.append(0)
	# data.append(255)
	# data.append(255)
	# data.append(0)
	# data.append(0)
	# data = data * (num_fixtures/2)
	# else:
	# try:
	# color = webcolors.hex_to_rgb(xkcd_names_to_hex[message])
	# except:
	# color = [randint(0, 255), randint(0, 255), randint(0, 255)]
	# data.append(color[0])
	# data.append(color[1])
	# data.append(color[2])
	# data = data * num_fixtures

if __name__ == "__main__":
    public.run(host='127.0.0.1:5000', debug=True)
