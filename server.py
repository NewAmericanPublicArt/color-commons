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
from math import sin
import itertools

wrapper = None

public = Flask(__name__)
public.config['PROPAGATE_EXCEPTIONS'] = True

# Include "no-cache" header in all POST responses
@public.after_request
def add_no_cache(response):
    if request.method == 'POST':
        response.cache_control.no_cache = True
    return response

### HOME PAGE API ###
@public.route('/') # DO we want to clarify methods=['GET']? ASK
@public.route('/index.html') # WILL take us fr / to /index.html, yes? ASK
def default_page():
    return render_template('/index.html')



def complement(color): # pass color as (r, g, b) tuple
    # simpler, slower version of http://stackoverflow.com/a/40234924
    return tuple(max(color) + min(color) - channel for channel in color)

def DmxSent(status):
    if status.Succeeded():
        print('Success!')
    else:
        print('Error: %s' % status.message, file=sys.stderr)

    global wrapper
    if wrapper:
        wrapper.Stop() # Shut down OLA transmission to DMX if wrapper's running ASK

def look_up_color(name):
    try:
        color = webcolors.hex_to_rgb(xkcd_names_to_hex[name])
    except: # if we can't find a color, make up a random one
        color = [randint(0, 255), randint(0, 255), randint(0, 255)]
    return color

## SMS API ##
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

    ip = "172.16.11.50"         # TODO - this is ours?
    port = 5000                 # UPnP TCP protocol
    message = "listentome"      # Yodel into the void
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (ip, port)) # Sends to own socket

    time.sleep(0.1)             # Waits on send request? Or for aesthetics
    global wrapper              # Whole other class for OLA!!!
    wrapper = ClientWrapper()
    client = wrapper.Client()
    client.SendDmx(universe, data, DmxSent)
    wrapper.Run()               # THROWS IT ALL TO THE PI TO RUN WITH
    return ('<?xml version="1.0" encoding="UTF-8" ?><Response></Response>')
                                # Giving back the texter some bull

# Initiator 
if __name__ == "__main__":
    public.run(host='127.0.0.1:5000', debug=True)
