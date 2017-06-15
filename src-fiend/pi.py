from __future__ import print_function
from flask import Flask, render_template, request
from uwsgidecorators import *
import time
from random import randint
import socket
from ola.ClientWrapper import ClientWrapper
import array
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
@public.route('/sms',method=['POST']):
def sendtoDmx():
    # NEED TO ACCESS BODY RESPONSE OBJECT - SHOULD be in format arr(12)
    ip = "172.16.11.50"
    port = 5000
    message = "listentome"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (ip, port))
    time.sleep(0.1) # Waiting for DMX to wake up
    global wrapper
    wrapper = ClientWrapper()
    client = wrapper.Client()
    client.SendDmx(universe, data, DmxSent) # OLA-standard call w closure
    wrapper.Run()
    return ('<?xml version="1.0" encoding="UTF-8" ?><Response>Success!</Response>')

def DmxSent(status):
    if status.Succeeded():
        print('Success!')
    else:
        print('Error: %s' % status.message, file=sys.stderr)

    global wrapper
    if wrapper:
        wrapper.Stop() # Shut down OLA transmission to DMX if wrapper's running ASK

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
