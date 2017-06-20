# File created by Brandon Stafford with help from Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of Raspberry Pi APP for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017

#from __future__ import print_function
#from uwsgidecorators import *

from flask import Flask, render_template, request
import time # Allows for Pharos to turn on
import socket
from ola.ClientWrapper import ClientWrapper # Allows for ACNstream, etc
import re # minimal regex support
import sys
import array
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

### PI'S HANDLING OF COLOR ARRAY ###
@public.route('/colors',methods=['POST'])
def sendtoDmx():
    colors = request.form['raw'] #request['raw']
    colors = convert_barr(colors)
    ip = "172.16.11.50"
    port = 5000
    init = "listentome"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(init.encode(), (ip, port))
    time.sleep(0.1) # Waiting for DMX to wake up
    global wrapper
    universe = 1 # For pharos fwdng
    wrapper = ClientWrapper()
    client = wrapper.Client()
    # DMXBUFFER CLASS - passes as array.array('B')
    client.SendDmx(universe, colors, DmxSent) # OLA-standard call w closure
    wrapper.Run()
    return ('<?xml version="1.0" encoding="UTF-8" ?><Response>Success!</Response>')

def DmxSent(status):
    if status.Succeeded():
        print('Success!')
#    else:
#        print('Error: %s' % status.message, file=sys.stderr)
    global wrapper
    if wrapper:
        wrapper.Stop() # Shut down OLA transmission to DMX if wrapper's running ASK

def convert_barr(input):
    # We have string of numbers as "11,12,13|10,9,8|etc..
    arr = re.split('\D+',input) # https://stackoverflow.com/questions/1059559/split-strings-with-multiple-delimiters
    arr = map(int,arr) # Converts to ints
    arr = array.array('B',arr) # Calls arr initializer as req'd
    return arr

# Initiator
if __name__ == "__main__":
    public.run(host='0.0.0.0', port=8080, debug=True)
