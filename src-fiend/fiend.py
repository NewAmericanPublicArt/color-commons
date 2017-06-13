# File created by Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of Linode APP for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017
from flask import Flask, render_template, request
# from uwsgidecorators import *
# import socket
# import sys

global app
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

# Include "no-cache" header in all POST responses
@app.after_request
def add_no_cache(response):
    if request.method == 'POST':
        response.cache_control.no_cache = True
    return response

# TEST API    
@app.route('/', methods=['GET'])
# @self.public.route('/index', methods=['GET'])	# Got em bleeding into each other - should work?
def serve():
    # Should be no body object passed
    return render_template('/data.html')

# SMS API - PASSES TO PI
@app.route('/sms', methods=['POST'])
def smser():
    return "Totally got sms post"

# Initiator 
if __name__ == "__main__":
	app.run(debug=True)

# USEFUL -
# @app.before_first_request
# def initialize():
#     print "Called only once, when the first request comes in"
