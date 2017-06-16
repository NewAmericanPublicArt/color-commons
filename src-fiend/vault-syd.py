#from __future__ import print_function
#from uwsgidecorators import *
import array

from flask import Flask, render_template, request
import time # Allows for Pharos to turn on
import socket
from ola.ClientWrapper import ClientWrapper # Allows for ACNstream, etc
import sys
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
    #
    return input

# Initiator
if __name__ == "__main__":
    public.run(host='0.0.0.0', debug=True)
