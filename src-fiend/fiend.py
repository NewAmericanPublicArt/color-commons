# FILE created by Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of FIEND class for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017
import array					# p_cmd array of 'B'
import calendar					# for month utils
from copy import deepcopy
import csv					# file entry/db format
import datetime					# get_date, get_time
import itertools				# p_cmd array/iterable loops
import json
from math import sin				# parse_command rainbow gen
import md5					# built-in hash
from random import randint                      # generate rand color
from rsrcs.names import *			# brings in NAMES, SURS
from rsrcs.xkcd_colors import xkcd_names_to_hex # look_up_color
import re					# regexing
import socket					#
import sys					#
import webcolors				#

class Fiend():
	
	# INITIALIZE

	def __init__(self,log,hash):
            self.log = log # Empty list of log entry
	    self.hasher = md5.new() # Establishes multipurpose md5 stream

	# DEEPCOPY CUSTOM HOOK - https://stackoverflow.com/a/15685014

	def __deepcopy__(self,memo={}):
	    # http://code.activestate.com/recipes/259179/
	    print("id of self.log is "+str(id(self.log)))
	    dcopy = Fiend(deepcopy(self.get_log()),None)
            print("id of dcopy.log is "+str(id(dcopy.log)))
            return dcopy

	# GETTERS

        def get_log(self):
            return self.log
	def get_time(self):
	   return datetime.datetime.time(datetime.datetime.now()) # TODO - incorp tzinfo, convert
	def get_date(self):
	   return datetime.date.today() # DATE hardwired naive; TODO convert format
	
	# IMPORT/EXPORT of CSV format

	def send_to_csv(self):
            log = open("log.csv",'w')
            for x in self.log:
                newline = str(x['name'])+","+str(x['msg'])+","+x['date']+","+x['time']+"\r\n"
                log.write(newline)
            log.close()

	def get_fr_csv(self,FILE):
	    if( self.get_log() != []): # No more than 1 file import allowed - can disable
		print("G_frCSV wont import")
		return
	    with open(str(FILE), 'rb') as csvfile:
		parse = csv.reader(csvfile, strict=True)
		next(parse,None) #Skips intro line
		for row in parse:# FILE looper
                    elem = {}
                    elem['name'] = str(row[0]).translate(None,'"') # name acquired
		    if len(row) is not 6:
		    	endmsg = False
		    	msg = row[2].translate(None, '|"')  # combine row[2] onwards till |
		    	for s in row[3:]:    
			    if not endmsg:
				s = str(s).translate(None,'"') #cleans
				if s.find('|') != -1:		
				    endmsg = True
				msg += s
			    else:
				msg = msg.translate(None,'|"') #rmv delim
				elem['msg'] = msg
				xdate = s
				break    
		    else:
			elem['msg'] = str(row[2]).translate(None,'|"') # remove delimiters
		        xdate = row[3]
		    dtime = self.convertexcel(xdate)
		    elem['date'] = dtime.date() 
		    elem['time'] = dtime.time()
		    if not (self.new_entry2(elem)):
			    print("Error pushing val to log")
		

	# LOADER for standardized week-old page info
	# We know; that self is untouched throughout all page refreshed (ID-based)
	# Also know; that hier object refreshes throughout (ID-changes)
	# So WHY at line 110 (following deepcopy) do we see access fr a DIFFERENT log? 	

	def load(self,optional):
	    hier = None
	    if optional is not None:	#file import optional
		self.get_fr_csv(optional);
	    hier = self.__deepcopy__() # TODO - access memo as [] framework?
	    hier.get_jsdt() # CONVERTER - check now
	    hier.log = hier.find(hier.log,{'date':{'start':(hier.get_date() - datetime.timedelta(days=6)),'end':(hier.get_date())}})
	    hier.log = hier.sort_by("day",hier.log)
	    for i, tier in enumerate(hier.log):
		hier.log[i] = hier.sort_by("color",tier) #assigns arr[] to ea var
	    return json.dumps(format)
	
	# MODIFIER takes log, creates new category ['jsdt'] for int values returned by get_ms - should exist in self
	
	def get_jsdt(self):
	    for x in self.get_log():
		x['jsdt'] = self.get_ms(x['date'],x['time'])

	# MODIFIER for exporting - strips ['date'] and ['time'] categories

	def rm_dt(self,hier):
	    for i,x in enumerate(hier):
		if type(x) is list: # needs nested call
		    hier[i] = self.rm_dt(x)
		elif type(x) is dict: # we are @ base level
		    del hier[i]['date']
		    del hier[i]['time']
	    return hier 

	# MODIFY/COPIER for exporting - changes to JSON format

	def to_hier(self):
	    depth = 0	
	    

	# ENTRY method for /sms POSTs: input validation executed here (1st line of defense)        

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

	# ALTERNATE ENTRY - for direct input from .csv files. See readme for proper format
	
	def new_entry2(self,elem):
	    # Elem should be of form {'name':w,'msg':x,'date':y,'time':z}
  	    if not(elem and ('name' in elem) and ('msg' in elem) and ('date' in elem) and ('time' in elem)):
                print("improper entry2 format")              
                return False
            elem['name'] = self.get_hashable(elem['name']) # No need for + removal
      	    self.log.append(elem)
	    return True

	# SEARCH HANDLER for dict-defined queries (automatically calls range suite)

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
	
	# RANGE HANDLER (automatically called by search handler)

	def range_find(self,arr,query):    
	    temp = []
	    for x in arr:
        	if ((query['name']==False or self.in_range(x['name'],query['name'])) and
		    (query['msg']==False or self.in_range(x['msg'],query['msg'])) and
                    (query['date']==False or self.in_range(x['date'],query['date'])) and
                    (query['time']==False or self.in_range(x['time'],query['time']))):
		    temp.append(x)
	    return temp


	# RANGE checker, returns a boolean T/F for single value/query in range/equivalent

	def in_range(self,elem,test):
	    if type(test) is dict:
		return ((elem>=test['start']) and (elem<=test['end']))
	    else:
		if (type(elem) is datetime.time) and (type(test) is datetime.time):
		    devi = datetime.timedelta(second=30) # Grabbing all within minute range
		    return (elem>=(test-devi) and elem<=(test+devi))
		else:
	            return (elem == test)
	
	# SORT method, returns a tree tier of lists

	def sort_by(self, root, raw):
	    SORTS = ["month","day","hour","users","newuser","color","color2"]
	    if root not in SORTS or raw is None or raw == []:
		return raw
	    else:
		tier = [] # RET item
	        if root is SORTS[0] or root is SORTS[1]:
	            ouryear = raw[0]['date'].year # And same for year
	    # MONTH sorts - assumes 12 always
		    if root is SORTS[0]: # by MONTH	
			for i in range(0,12):
			    bmo = datetime.date(ouryear, (i+1), 1)# begin month
			    emo = datetime.date(ouryear, (i+1), calendar.monthrange(ouryear,(i+1))[1])
		            tier.append(self.find(raw,{'date':{'start':bmo,'end':emo}}))
	    # DAY sorts - uses compute_range TODO - ensure all dates (not just ones w texts) include
		    elif root is SORTS[1]:
		        daylist = self.compute_range(raw,'date')
		    	for x in daylist:
			    tier.append(self.find(raw,{'date':x})) # consider - removal fr main to avoid olap
	    # HOUR sorts - separate TIME item from DATE
		elif root is SORTS[2]: #BY 24-HR, 1/24 CATEGORIES
		    for i in range(0,24):
			temp = [datetime.time(i,0,0),datetime.time(i,59,59)]
			tier.append(self.find(raw,{'time':{'start':temp[0],'end':temp[1]}}))
	    # USERS sorts - parses down to unique subset of USERS
		elif root is SORTS[3]: # UNIQUE users
		    for i in raw[:]:
                        found = False
			for j in tier[:]:
			    if (i['name'] == j['name']): # EQ compare, not ID
				found = True
			if not found:
			    tier.append(i) # Adds as new j entry, restarts i-iter
            # UNIQUE USERS sort - parses from USERS subset to UNIQUE users subset
		elif root is SORTS[4]: # NEW UNIQUE users
		    tier = self.sort_by("users",raw) # ranged unique users for our set
		    bot = datetime.date(2013,1,1)
		    top = (min(raw, key=lambda x:x['date']))['date'] # defines all val BEFORE raw
		    top = top - datetime.timedelta(days = 1) # Should reset BEFORE line far enough		
		    B = self.sort_by("users",(self.find(None,{'date':{'start':bot,'end':top}}))) # comp gainst prev vals    
		    for i in tier[:]: # [SO]/questions/742371/python-strange-behavior-in-for-loop-or-lists
			for j in B[:]:
			    if (i['name'] == j['name']):
				tier.remove(i)
                  		if tier is None: #rmv? TODO
	   			    print("empty tier")
	    # COLORS sort - parses down to unique subset of MSGs
  		elif root is SORTS[5] or root is SORTS[6]:
	    	    colorlist = sorted(self.compute_range(raw,'msg'))
		    for i,x in enumerate(colorlist):
		        tier.append(self.find(raw,{'msg':x}))
	    # COLORISH sort - parse down to VAGUELY CLOSE unique subsets of msgs	
		    if root is SORTS[6]:
			# DO THINGS TO TIER ITSELF - we know that we can go right into
			print("special colors not made yet")    		    
		else:
		    print("SORT_BY: Haven't heard of that one!")
		return tier
	
	# helper which takes set of data & returns list of (nonrepeat) dates for assembly
	def compute_range(self,raw,key):
	    range = []
	    for i in raw[:]:
		found = False
		for j in range: 
		    if (i[key] == j):
			found = True
		if not found:
		    range.append(i[key])
	    return range

	# OPTIONAL function call - cleans empty list creations (ie, range MO:2-10 will gen arr[12] with empty)
	def clean_sort(self,raw):
	    return filter(None, raw)

	# HASHING/ALIAS methods (MD5-compliant)
	
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
	
	# MULTIPURPOSE methods - unrelated to self object
	
	# CONVERTER:date obj and/or time object=> int representing total milliseconds fr UTC-std start
	
	def get_ms(self,d,t): # gets in MS; optional D & T entries, if both included adds the 2
	    dstd = datetime.date(1970,1,1)
	    if d is None:
		secs = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds() 
	    elif t is None:
		secs = (d - dstd).total_seconds()
	    else:
		secs = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds()
		secs += (d - dstd).total_seconds()
	    return int(secs * 1000)

	# CONVERTER:string of "HH:MM:SS YR-MO-DA ..."format => py datetime.datetime obj
	
	def convertexcel(self,raw):
	    raw = raw.strip('"')
	    raw = raw.split(' ',1) #maxsplit property splits date/time
	    dat = raw[0]
	    tim = raw[1]
	    yr,mo,day = dat.split('-')
	    hr,min,sec = tim.split(':')
	    sec = (sec.split(' '))[0]
	    dtime = datetime.datetime(int(yr),int(mo),int(day),int(hr),int(min),int(sec))
	    return (dtime - datetime.timedelta(hours=4)) # CONVERT from UTC format to boston

	# CONVERTER:tuple of RGB tuples => string with x,y,z|a,b,c|...format
	
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

	# PARSER for PHAROS lights display

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
	
	# COLOR methods (access, complement)

	def complement(self, color): # pass color as (r, g, b) tuple
	    # simpler, slower version of http://stackoverflow.com/a/40234924
	    return tuple(max(color) + min(color) - channel for channel in color)

	def look_up_color(self, name):
	    try:
		color = tuple(webcolors.hex_to_rgb(xkcd_names_to_hex[name]))
	    except: # if we can't find a color, make up a random one
		color = (randint(0, 255), randint(0, 255), randint(0, 255))
	    return color
