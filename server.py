from __future__ import print_function
from flask import Flask, render_template, request
from uwsgidecorators import *
from xkcd_colors import xkcd_names_to_hex
import webcolors
import time

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
    message = request.form['Body']
    print("Received text message: " + str(message))
    color = webcolors.hex_to_rgb(xkcd_names_to_hex[str(message.lower())])
    cmd = str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + '\n'
    universe = 1
    num_fixtures = 24
    data = array.array('B')
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

    # send DMX here
    print('Wrote to USB: {0}'.format(cmd))
    return ('<?xml version="1.0" encoding="UTF-8" ?><Response></Response>')

# @public.route('/sms', methods=['POST'])
# def control_lights():
#     d = {'airforceblue': '11',
#         'airsuperiorityblue': '11',
#         'aliceblue': '16',
#         'youcompletemelights': '92',
#         'zebra': '93'}
#     allowed_commands = ['X040A',
#         'X040B',
#         'X0462']
#     import random
#     message = request.form['Body']
#     print "Received text message: " + str(message)
#     try:
#         program = int(d[message[0:25].lower().replace(' ', '')])
#     except KeyError:
#         print 'color {0} not found'.format(message)
#         program = random.randint(10,98)
#     command = 'X04%(number)2.2X' % {"number": program}
#     print 'Translated {0} to {1}'.format(message, command)
#     if (command in allowed_commands):
#         pytronics.serialWrite(command, speed=9600)
#     else:
#         print "Command {0} is not one of the allowed commands.".format(command)
#         command = 'FAIL'
#     return('<?xml version="1.0" encoding="UTF-8"?><Response>{0}</Response>'.format(command))

if __name__ == "__main__":
    public.run(host='127.0.0.1:5000', debug=True)
