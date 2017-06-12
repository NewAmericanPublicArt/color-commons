# File created by Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of FIEND class for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017
from flask import Flask, render_template, request
#from uwsgidecorators import *

## FIEND CLASS AND RELATED FUNCTIONS ##

# Specified conditional find - hardwired for particular object
# See how nasty this is? Trying to separate from declaration
def conditional_find(arr,test):
        temp = []
        for x in arr:
            if ((x['name']==test['name'] or test['name']==False) and
                (x['msg']==test['msg'] or test['msg']==False) and
                (x['stamp']==test['stamp'] or test['stamp']==False)):
                temp.append(x)
        return temp

# Sanitize function - uses encode & decode modules of strings
# Suggestion from Vasily Alexeev
# https://stackoverflow.com/questions/8689795/how-can-i-remove-non-ascii-characters-but-leave-periods-and-spaces-using-python#comment72965907_18430817
def sanitize(input):
    return input.decode('utf-8').encode('ascii',errors='ignore')

# FIEND CLASS - CONTROLS RPI, ETC FROM LINODE SERVER
class Fiend:

    def __init__(self):

        self.log = [] # Empty dict of log entries TODO replace w flask db!!!
        self.app = Flask(__name__)
        self.app.config['PROPAGATE_EXCEPTIONS'] = True
        self.app.add_url_rule('/','index',self.index_rt)
        self.app.add_url_rule('/','sms',self.sms_rt)

        self.app.run(debug=True)

    def index_rt(self):
            return ('<?xml version="1.0" encoding="UTF-8" ?><Response>GET SERVED!</Response>')

    def sms_rt(self):
        return "SMS CALLED PASERON"

    def new_entry(self,elem):
        # Elem should be of type {'name':'x','msg':'y','stamp':'z'}
        if elem:
            if not (('name' in elem) and
                 ('msg' in elem) and
                 ('stamp' in elem)):
                print("improper entry format")
                return False
        elem['msg'] = sanitize(elem['msg'])
        self.log.append(elem)
        return True

    def find(self,query): # Returns a list of terms matching query
        found = []
        if query: #Essentially generates placeholders for cond_find
                if 'name' not in query:
                        query['name'] = False
                if 'msg' not in query:
                        query['msg'] = False
                if 'stamp' not in query:
                        query['stamp'] = False
                found = conditional_find(self.log,query)
        else:
            return self.log
        return found #if !query, returns empty list

    def log_csv(self,filex):
        return filex
        # Loads SEVERAL entries from preexisting/compiled fr Twilio
    def to_csv(self):
        return filex