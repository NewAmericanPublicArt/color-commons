# FILE created by Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of FIEND class for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017

from xkcd_colors import xkcd_names_to_hex 	# look_up_color
from random import randint			# generate rand color
import socket					#
from math import sin				# parse_command rainbow gen
import itertools				# p_cmd array/iterable loops
import array					# p_cmd array of 'B'
import sys					#
import webcolors				# look_up_color
import datetime					# get_date, get_time
import md5					# get_hashable

# FIEND CLASS
# CONTROLS RPI FROM LINODE SERVER

class Fiend():
	
	def __init__(self):
            self.log = [] # Empty dict of log entry
	    self.hasher = md5.new() # Establishes multipurpose md5 stream
	
	# Getters
	def get_time(self):
	   return datetime.datetime.time(datetime.datetime.now()) # TODO - incorporate tzinfo, convert format
	def get_date(self):
	   return datetime.date.today() # DATE hardwired naive; TODO convert format
	def get_dict(self):
	    return self.log
	
	# Generator for new log items - majority of input validation executed here
        def new_entry(self,elem):
            # Elem should be of type {'name':'x','msg':'y'}
            if not(elem and ('name' in elem) and ('msg' in elem)):
                print("improper entry format")
                return False
	    elem['name'] = self.get_hashable(elem['name'])
            elem['date'] = self.get_date() #Bc TWILIO does not provide a timestamp when SENT
            elem['time'] = self.get_time() #It is worth noting that these are times RECEIVED
            self.log.append(elem) # Elem is in type {'name':'x','msg':'y','date':x,'time':y}
            return True
     
	# Interacts with incomplete/variable-length queries
	def find(self,entry):
	    found = []
	    if query: #Essentially generates placeholders for cond_find
                if 'name' not in query:
             	   query['name'] = False
                if 'msg' not in query:
                   query['msg'] = False
                if 'date' not in query:
                   query['date'] = False
		if 'time' not in query:
		   query['time'] = False
                found = conditional_find(self.log,query)
            return found # if !query, returns empty list
	
	# Aggregator given all fields ( groomed by FIND() )
	def conditional_find(arr,test):
            temp = []
            for x in arr:
            	if ((x['name']==test['name'] or test['name']==False) and
               	    (x['msg']==test['msg'] or test['msg']==False) and
                    (x['date']==test['date'] or test['date']==False) and
	            (x['time']==test['time'] or test['time']==False)):
           	   temp.append(x)
            return temp
	
	# MD5-compliant hashing & indexing functions
	
	def get_hashable(self,nos):
	    self.hasher.update(str(nos)) # Feeds #s as str
	    hex = self.hasher.hexdigest()# Spits out encoded str
	    alias = self.generate_alias(hex)# Cross-indexes w extant baby names	   
	    return alias	    
	
	def generate_alias(self,hash):
	    # TODO - THIS FUNCTION CROSS-REFERENCES W 2 LISTS ND LAST 4 DIGITS
	    return "Capt. Bev"	
	
	# MULTIPURPOSE functions - unrelated to self object 
	
	def parse_command(self, message):
	    FIXTURES = 24
	    populate = True
	    data = [] # Starts life as an array object
	    if(message == "secret"):
		data.append((0,0,255)) # top
		data.append((255,0,0)) # bot	
	    elif(message == "flip white"):
                data.append((255,255,255))
                data.append((0,0,0))
	    elif(message == "flip black"):
                data.append((0,0,0))
                data.append((255,255,255))
	    elif(message == "rainbow"):
		data = [(int(128 + 128 * sin(phase)), \
			 int(128 + 128 * sin(2.094 + phase)), \
			 int(128 + 128 * sin(4.189 + phase))) \
		for phase in [x/1000.0 for x in range(0, 6282, 6282/FIXTURES)]]
	    	del data[(FIXTURES):] # TRIMS - was @ 75 generated (BRANDON?)
		populate = False
	    elif(message.startswith("flip")):
		remainder = message[4:].strip() # chop off flip and strip any spaces
		color = self.look_up_color(remainder)
		inverse = self.complement(color)
		data.append(color)
		data.append(inverse)
	    else:
		color = self.look_up_color(message) #rets (x,y,z)(x,y,z)
		data.append(color)
		data.append(color)
	    # FORMAT data from 2 RGB tuples to chain of (24*3) numbers  
   	    if (populate):	
		data = data * (FIXTURES/2)
            # DO STUFF HERE TO CHANGE INTO A ARRAY.ARRAY?
	    data = array.array('B', itertools.chain.from_iterable(data))
	    return data

	def complement(self, color): # pass color as (r, g, b) tuple
	    # simpler, slower version of http://stackoverflow.com/a/40234924
	    return tuple(max(color) + min(color) - channel for channel in color)

	def look_up_color(self, name):
	    try:
		color = tuple(webcolors.hex_to_rgb(xkcd_names_to_hex[name]))
	    except: # if we can't find a color, make up a random one
		color = (randint(0, 255), randint(0, 255), randint(0, 255))
	    return color

	def convert_to_str(self, arr):
	    condensed = ""
	    last = len(arr)-1
	    for i, x in enumerate(arr):
		condensed+=str(x)
		if ((i%3==2) and (i!=last)):
		    condensed+="|"
		elif (i!=last):
		    condensed += ","
		# Else, add nothing - last values
	    return condensed
