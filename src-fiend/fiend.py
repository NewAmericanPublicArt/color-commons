# FILE created by Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of FIEND class for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017

from xkcd_colors import xkcd_names_to_hex 	# look_up_color
from random import randint			# generate rand color
from names import *				# brings in NAMES, SURS
import socket					#
from math import sin				# parse_command rainbow gen
import itertools				# p_cmd array/iterable loops
import array					# p_cmd array of 'B'
import re					# regexing
import sys					#
import webcolors				# look_up_color
import datetime					# get_date, get_time
import calendar
import csv					# file format
import md5					# get_hashable
import xlrd					# PACKAGE for excel date conv

# FIEND CLASS
# CONTROLS RPI FROM LINODE SERVER

class Fiend():
	
	def __init__(self):
            self.log = [] # Empty list of log entry
	    self.hasher = md5.new() # Establishes multipurpose md5 stream

	# Getters
	def get_time(self):
	   return datetime.datetime.time(datetime.datetime.now()) # TODO - incorp tzinfo, convert
	def get_date(self):
	   return datetime.date.today() # DATE hardwired naive; TODO convert format
	def get_log(self):
	    return self.log
	
	# IMPORT/EXPORT function

	def send_to_csv(self):
            log = open("log.csv",'w')
            for x in self.log:
                newline = str(x['name'])+","+str(x['msg'])+","+x['date']+","+x['time']+"\r\n"
                log.write(newline)
            log.close()

	def get_fr_csv(self,FILE):
	    with open(str(FILE), 'rb') as csvfile:
		parse = csv.reader(csvfile, strict=True)
		next(parse) #Skips intro line
	    	for row in parse:
		    if len(row) is not 6:
			print(row)
		    else:
			elem = {}
			elem['name'] = str(row[0])
			elem['msg'] = str(row[1]).translate(None,'|') # remove delimiters
			
			elem['date'] = 0
			elem['time'] = 0
	    		if not (self.new_entry2(elem)):
			    print("Error pushing val to log")

	# GENERATE new log entries: input validation executed        

	def new_entry(self,elem):
            # Elem should be of type {'name':'x','msg':'y'}
            if not(elem and ('name' in elem) and ('msg' in elem)):
                print("improper entry format")
                return False
	    elem['name'] = elem['name'].translate(None,'+')
	    elem['name'] = self.get_hashable(elem['name'])
            elem['date'] = self.get_date() #Bc TWILIO does not provide a timestamp when SENT
            elem['time'] = self.get_time() #It is worth noting that these are times RECEIVED
            self.log.append(elem) # Elem is in type {'name':'x','msg':'y','date':x,'time':y}
            return True

	# ALTERNATE ENTRY - for testing purposes
	def new_entry2(self,elem):
	    # Elem should be of form {'name':w,'msg':x,'date':y,'time':z}
  	    if not(elem and ('name' in elem) and ('msg' in elem) and ('date' in elem) and ('time' in elem)):
                print("improper entry2 format")
                return False
            elem['name'] = self.get_hashable(elem['name']) # No need for + removal
      	    self.log.append(elem)
	    return True

	# HANDLER for dict-defined queries

	def find(self,arr,query):
	    found = self.log # Uneccessary assignment - note bottom functional for ALL implementation
	    if query: #Essentially generates placeholders for cond_find
                if 'name' not in query:
             	   query['name'] = False
                if 'msg' not in query:
                   query['msg'] = False
                if 'date' not in query:
                   query['date'] = False
		if 'time' not in query:
		   query['time'] = False 

                if arr is None:
		    found = self.range_find(found,query) #More precise range find
	        else:
		    found = self.range_find(arr,query)
	    return found # if !query, returns full list
	
	# AGGREGATOR for SEARCH through given arr

	def range_find(self,arr,query):
	    temp = []
	    for x in arr:
		if ((query['name']==False or self.in_range(x['name'],query['name'])) and
		    (query['msg']==False or self.in_range(x['msg'],query['msg'])) and
                    (query['date']==False or self.in_range(x['date'],query['date'])) and
                    (query['time']==False or self.in_range(x['time'],query['time']))):
		    temp.append(x)
	    return temp

	# RANGE checker, returns a boolean

	def in_range(self,elem,test):
	    if 'start' in test:
		return ((elem>=test['start']) and (elem<=test['end']))
	    else:
		if (type(elem) is datetime.time) and (type(test) is datetime.time):
		    # For now, we will get it within the 10min range TODO - MOD OVER 60, THEN ADD/SUB HR AS NEEDED
		    return (test.hour == elem.hour and (elem.minute>=(test.minute-5)) and (elem.minute<=(test.minute+5))) 
#		elif type(val) is datetime.date:
		else:
	            return (elem == test)
	
	# SORT function, returns a tree tier of lists

	def sort_by(self, root, raw):
	    SORTS = ["month","day","hour","users","newuser"]
	    if root not in SORTS:
		return raw
	    else:
		tier = [] # RET item
		if root is SORTS[0] or root is SORTS[1]: # need date object vals
		    ourmonth = raw[0]['date'].month # Assume vals within same month - ONLY ACCESSED by day
                    ouryear = raw[0]['date'].year # And same for year
		    if root is SORTS[0]: # by MONTH	
			for i in range(0,12):
			    bmo = datetime.date(ouryear, (i+1), 1)# begin month
			    emo = datetime.date(ouryear, (i+1), calendar.monthrange(ouryear,(i+1))[1])
		            tier.append(self.find(raw,{'date':{'start':bmo,'end':emo}}))
		    elif root is SORTS[1]:		#30-DAY, 1/30 BY MONTH
		    	for i in range(0, calendar.monthrange(ouryear,ourmonth)[1]):
		            print(i)
			    day = datetime.date(ouryear, ourmonth, (i+1))
			    tier.append(find(raw,{'date':day}))
		elif root is SORTS[2]: #BY 24-HR, 1/24 CATEGORIES
		    for i in range(0,24):
			temp = [datetime.time(i,0,0),datetime.time(i,59,59)]
			tier.append(find(raw,{'time':{'start':temp[0],'end':temp[1]}}))
		elif root is SORTS[3]: # UNIQUE users
		    for i in raw:
                        found = False
			for j in tier:
			    if (i['name'] == j['name']): # EQ compare, not ID
				found = True
			if not found:
			    tier.append(i) # Adds as new j entry, restarts i-iter
		elif root is SORTS[4]: # NEW UNIQUE users
		    tier = self.sort_by("users",raw) # ranged unique users for our set
		    bot = datetime.date(2013,1,1)
		    top = (min(raw, key=lambda x:x['date']))['date'] # defines all val BEFORE raw
		    top = top.replace(day=top.day-1)
		    print("calculated earliest = "+str(top))			
		    B = self.find(None,{'date':{'start':bot,'end':top}}) # comparing against prev vals
		    
		    for i in tier[:]: # [SO]/questions/742371/python-strange-behavior-in-for-loop-or-lists
			for j in B:
			    if (i['name'] == j['name']):
				tier.remove(i)
		return tier

	# OPTIONAL function call - cleans empty list creations (ie, range MO:2-10 will gen arr[12] with empty)
	def clean_sort(self,raw):
	    return filter(None, raw)

	# MD5-compliant HASHER & indexing functions
	
	def get_hashable(self,nos):
	    nos = re.sub("[^0-9]",'',nos) #rmvs + from Twilio formatting
	    self.hasher.update(nos) # Feeds #s as str
	    hex = self.hasher.hexdigest()# Spits out encoded str
	    alias = self.generate_alias(hex)# Cross-indexes w extant baby names	   
	    return alias	    
	
	def generate_alias(self,hash):
	    KEY_LEN = 32
	    SUR_LEN = 2 # front 2 chars
	    NAME_LEN = 27 # middy 27 chars	
	    TAG_LEN = 3 # back 3 chars
	    key = int(hash,16)
	    # Bit manipulation to isolate chunks of hex
	    surkey = (key >> ((KEY_LEN - SUR_LEN)*4))	    
	    namekey = ((key << (SUR_LEN*4)) >> (TAG_LEN*4))
	    tagMASK = 4095
	    tagtrail = ("%x" % (key & tagMASK))[-3:] #Strips/rets last 3 vals	
	    surkey = surkey % (len(SURS))	# 256 mod ~25 - CHANGES W NAMES.PY
	    namekey = namekey % (len(NAMES))	# [16]^(27 chars) mod ~2000  
	    alias = SURS[surkey] + " " + NAMES[namekey]	+ "-" + tagtrail
	    return alias

	# MULTIPURPOSE functions - unrelated to self object 
	
	# PARSER for PHAROS

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
