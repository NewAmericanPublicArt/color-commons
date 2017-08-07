# FILE created by Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of FIEND class for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017
import array					# p_cmd array of 'B'
import calendar					# for month utils
from copy import deepcopy
import csv						# file entry/db format
import datetime					# get_date, get_time
import itertools				# p_cmd array/iterable loops
import json
from math import sin			# parse_command rainbow gen
from hashlib import md5			# built-in hash
from random import randint      # generate rand color
from resources.names import *	# brings in NAMES, SURS
from resources.xkcd_colors import xkcd_names_to_hex # look_up_color
import re						# regexing
import socket					#
import sys						#
import webcolors				#

class Fiend():
	
	# INITIALIZE
	def __init__(self,log,hash):
		self.log = log # Empty list of log entry
		self.hasher = md5() # Establishes multipurpose md5 stream
		self.SORTS = ["month","week","day","hour","user","newuser","color","color2"]
		self.SPECS = ["on","range","since"]	

	# DEEPCOPY CUSTOM HOOK - https://stackoverflow.com/a/15685014
	def __deepcopy__(self,memo={}):# http://code.activestate.com/recipes/259179/
		dcopy = Fiend(deepcopy(self.get_log()),None)
		return dcopy

	# GETTERS
	def get_log(self):
		return self.log
	def get_time(self):
		return datetime.datetime.time(datetime.datetime.now()) # TODO - incorp tzinfo, convert
	def get_date(self):
		return datetime.date.today() # DATE hardwired naive; TODO convert format
	
#-------IMPORT/EXPORT of CSV format

	def send_to_csv(self):
		newlog = open("log.csv",'w')
		for x in self.log:
			newline = str(x['name'])+","+str(x['msg'])+","+x['date']+","+x['time']+"\r\n"
			newlog.write(newline)
		newlog.close()

	def get_fr_csv(self,FILE):
		if( self.get_log() != []): # No more than 1 file import allowed - can disable
			print("frCSV:No import\n")
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
					print("Error pushing "+str(elem)+" to log\n")
	
#-------DIRECT API ENTRY method for /sms POST       

	def new_entry(self,elem):
        # Elem should be of type {'name':'x','msg':'y'}
		if not(elem and ('name' in elem) and ('msg' in elem)):
			print("N_E:Improper entry format\n")
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
			print("N_E2:Improper entry2 format\n")              
			return False
		elem['name'] = self.get_hashable(elem['name']) # No need for + removal
		self.log.append(elem)
		return True
	
#-------LOADER for page information by category
	
	def load(self,optional,args):

		if optional is not None: # file import optional
			self.get_fr_csv(optional)

		hier = self.__deepcopy__()
		hier.get_jsdt() # CONVERTER
		s = [False, False] # skip value; max 2
		query = {}
		treed = False
		for i, arg in enumerate(args):
			if (s[0]^s[1] is False):
				if arg in self.SPECS: # Depending on what it is, grabs 1-2 of next vals
					s[0] = True # At least 1 skip
					if arg is self.SPECS[0]: # "on"
						q = args[i+1]
						if (type(q) is datetime.date):
							query['date'] = q
						elif (type(q) is datetime.time):
							query['time'] = q
						else:
							print("Improper follower to ON")
							return None
					elif arg is self.SPECS[1]: # "range"
						s[1] = True
						q0 = args[i+1]
						q1 = args[i+2]
						q = {'start':q0, 'end':q1}
						if (type(q0) is datetime.time & type(q1) is datetime.time):
							query['time'] = q
						elif (type(q0) is datetime.date & type(q1) is datetime.date):
							query['date'] = q
						else:
							print("Improper/unmatched followers to RANGE")
							return None
					else: # self.SPECS[2] "since"
						q0 = args[i+1]
						if (type(q0) is datetime.time):
							q1 = self.get_time()
							query['time'] = {'start':q0,'end':q1}
						elif (type(q0) is datetime.date):
							q1 = self.get_date()
							query['date'] = {'start':q0,'end':q1}
						elif (q0 in self.SORTS): #special "Since" w sorts handler
							key = q0
							if (key in self.SORTS[:3]):
								q0 = self.get_date()
								if (key is self.SORTS[0]): #month
									q1 = q0 - datetime.timedelta(months=1) # TODO -right span?
								elif (key is self.SORTS[1]): #week
									q1 = q0 - datetime.timedelta(days=6) 
								elif (key is self.SORTS[2]): #day
									q1 = q0 - datetime.timedelta(days=1)
								query['date'] = {'start':q1, 'end':q0}
							elif (key is self.SORTS[3]): #hour
								q0 = self.get_time()
								q1 = q0 - datetime.timedelta(hours=1)
								query['time'] = {'start':q1, 'end':q0}
							else: #othersort
								print("Improper usage of SINCE")
								return None
						else:
							print("Improper follower to SINCE")
							return None
				elif arg in self.SORTS:
					if (treed is False): # Transition over fr FIND to SORT
						treed = True
						dataset = hier.find(None,query) # ACTUALLY IMPLEMENTS above query-builder
						hier.log = {'name':hier.tierlabel(None,query), 'children':hier.sort_by(arg,dataset)}
						print("181 "+str(hier.log)[:800])
					else:
						print("2nd sort for "+arg)
						print("183 "+str(hier.log)[:800])
						hier.log = hier.nodeloop(hier.get_log(),arg) 		
						print("185 "+str(hier.log))			 
				else:
					print("Improper usage of LOAD; unknown key")
			elif (s[1] is True): # Function as skippers for 1-2 terms given specialty criteria
				s[1] = False
			else: # Know that s[0] is true
				s[0] = False

		if (treed is False): #last-minute combing
			hier.log = {'name':hier.tierlabel(None,query), 'children':hier.find(None,query)} #IMPLEMENTS w/o sort			
		
		hier.rm_dt(hier.get_log())
		print("197 "+str(hier.get_log())[:800])
		return hier.log

	def nodeloop(self, node, arg):
		if ('children' in node):
			if (node['children'] == []): #Empty branch
				print("empty parent")
				return node # dont do anyth to it
			if ('msg' in node['children'][0]): # Actual call
				print("lil sorting "+node['name'])
				node = self.sort_by(node,arg) #Call on entire object for all leaves
				return node
			else: #Go down a nest in a loop
				print("big sorting "+node['name'])
				for elem in node['children']:
					elem = nodeloop(elem,arg)
				return node
		else:
			print("got leaf")

	def tierlabel(self, arg, data):
		if (arg is self.SORTS[0]): #month - passed 1-12 int
			return(calendar.month_abbr[data])
		elif (arg is self.SORTS[1]): #week - passed datetime start date
			return("Week of"+calendar.day_abbr[data.weekday()]+" "+self.daylabel(data.day))
		elif (arg is self.SORTS[2]): #day - passed datetime date
			return(calendar.day_abbr[data.weekday()]+" "+self.daylabel(data.day))
		elif (arg is self.SORTS[3]): #hr - passed 0-24(?) int
			return("hr"+str(data)) #user,nuser - passed obj
		elif (arg is self.SORTS[4] or arg is self.SORTS[5]): #user - passed obj
			return(data['name']) #color, colorish - passed str
		elif (arg is self.SORTS[6] or arg is self.SORTS[7]): #color
			return(data)
		elif (type(arg) is dict): #query object
			tripped = False #for spacing
			label = ""
			
			if ('msg' in arg):
				tripped = True
				if ('start' in arg['msg']):
					label += "Colors ranged from "+arg['msg']['start']+" to "+arg['msg']['end']
				else:
					label += "Only "+arg['msg']

			if ('name' in arg):
				if (tripped == False):
					tripped = True
				else:
					label += " "
				if ('start' in arg['name']):
					label += "Names ranged from "+arg['name']['start']+" to "+arg['name']['end']
				else:
					label += "By "+arg['name']

			if ('date' in arg):
				if (tripped == False):
					tripped = True
				else:
					label += " "
				if ('start' in arg['date']): # Ranged
					label += "From "+self.tierlabel("day",arg['date']['start'])+" to "+self.tierlabel("day",arg['date']['end'])
				else:
					label += "On "+self.tierlabel("day",arg['date'])

			if ('time' in arg):
				if (tripped == False):
					tripped = True
				else:
					label += " "
				if ('start' in arg['time']):
					label += "From "+self.tierlabel("hour",arg['time']['start'].hour)+" to "+self.tierlabel("hour",arg['time']['end'])
				else:
					label += "On "+self.tierlabel("hour",arg['time'].hour)

			return label





#	def defaultload(self,optional):
#		if optional is not None:	#file import optional
#		self.get_fr_csv(optional)
#		hier = self.__deepcopy__()
#		hier.get_jsdt() # CONVERTER - check now
#		dataset = hier.find(hier.log,{'date':hier.get_date()})
#           dataset = hier.sort_by("hour",dataset) # Converts fr [] to [{x,[]},{y,[]}...
#		for i,hr in enumerate(dataset):
#		dataset[i]['children'] = hier.sort_by("user",hr['children']) #assigns arr[] to ea var
#		hier.rm_dt(dataset)
#		format = { 'name':(calendar.day_abbr[hier.get_date().weekday()]+" the "+self.daylabel(hier.get_date().day)),'children': dataset }
#		return json.dumps(format) 
	
	def defaultload(self, optional):
		return self.load(optional,['since','day','hour','user'])

	def sampleload(self, optional):
		return self.load(optional, ['on',datetime.date(2017,7,27),'hour','user'])	

#-------SEARCH HANDLER for dict-defined queries (automatically calls range suite)

	def find(self,arr,query):
		found = self.log
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
	
#-------SORT method, returns a tree tier of lists **w modified JSON hierarchy

	def sort_by(self, root, raw):
		if root not in self.SORTS or raw is None or raw == []:
			return raw
		else:
			tier = [] # RET item
			if type(raw) is dict:
				raw = raw['children'] # Focuses on important component for reference
			if root is self.SORTS[0] or root is self.SORTS[1]:
				ouryear = raw[0]['date'].year # And same for year
		# MONTH sorts - assumes 12 always
				if root is self.SORTS[0]: # by MONTH	
					for i in range(0,12):
						bmo = datetime.date(ouryear, (i+1), 1)# begin month
						emo = datetime.date(ouryear, (i+1), calendar.monthrange(ouryear,(i+1))[1])
						tier.append({ 'name': self.tierlabel(root,(i+1)), 'children': self.find(raw,{'date':{'start':bmo,'end':emo}})})
		# WEEK sorts
				elif root is self.SORTS[1]: # by WEEK
					daylist = sorted(self.compute_range(raw,'date'))
					startdate = self.compute_mon(daylist[0]) # Grabs 1st date
					enddate = daylist[(len(daylist)-1)] # Grabs last date
					while (startdate < enddate): # THIS DECISION allows for full-week completion
						weekset = []
						for i in range(0,7):
							offset = startdate + datetime.timedelta(days=i)
							weekset += self.find(raw,{'date':offset})
						dcopy = deepcopy(weekset) # TODO - not sure this is essential
						tier.append({'name': self.tierlabel(root,startdate), 'children': dcopy })
		# DAY sorts - uses compute_range
			elif root is self.SORTS[2]:
				daylist = self.compute_range(raw,'date')
				for x in daylist:
					tier.append({ 'name': self.tierlabel(root,x), 'children': self.find(raw,{'date':x})}) # consider - removal fr main to avoid olap
		# HOUR sorts - separate TIME item from DATE
			elif root is self.SORTS[3]: #BY 24-HR, 1/24 CATEGORIES
				for i in range(0,24):
					temp = [datetime.time(i,0,0),datetime.time(i,59,59)]
					tier.append({ 'name': self.tierlabel(root,i), 'children': self.find(raw,{'time':{'start':temp[0],'end':temp[1]}})})
			# USERS sorts - parses down to unique subset of USERS
			elif root is self.SORTS[4]: # UNIQUE users
				for i in raw[:]: 
					found = False
					for iter,j in enumerate(tier[:]):
						if (i['name'] == j['name']): # EQ compare, not ID
							found = True
							tier[iter]['children'].append(i) # Add to specific user iter
					if not found:
						tier.append({'name': self.tierlabel(root,i), 'children':[i]}) # Adds as new j entry, restarts i-iter
        # UNIQUE USERS sort - parses from USERS subset to UNIQUE users subset
			elif root is self.SORTS[5]: # NEW UNIQUE users
				tier = self.sort_by("users",raw) # ranged unique users for our set
				bot = datetime.date(2013,1,1)
				top = (min(raw, key=lambda x:x['date']))['date'] # defines all val BEFORE raw
				top = top - datetime.timedelta(days = 1) # Should reset BEFORE line far enough		
				B = self.sort_by("users",(self.find(None,{'date':{'start':bot,'end':top}}))) # comp gainst prev vals    
				for i in tier[:]: # [SO]/questions/742371/python-strange-behavior-in-for-loop-or-lists
					for j in B[:]:
						if (i['name'] == j['name']):
							tier.remove(i)
        # COLORS sort - parses down to unique subset of MSGs	
			elif root is self.SORTS[6] or root is self.SORTS[6]:
				colorlist = sorted(self.compute_range(raw,'msg'))
				for x in colorlist:
					tier.append({'name': self.tierlabel(root,x), 'children': self.find(raw,{'msg':x})})
		# COLORISH sort - parse down to VAGUELY CLOSE unique subsets of msgs	
				if root is self.SORTS[7]:
					tierish = []
					for branch in tier:
						branch['name'] = branch['name'].strip().lower() # TODO - remove bc only really needed for csvs
					# Then combine prompts with matching
					for i,b1 in enumerate(tier[:]):
						elem = b1['name']
						for j,b2 in enumerate(tier[:]):
							if ((i!=j) and (elem==b2['name'])):
								b1['children']+=b2['children']
								tier.remove(b2)
		# ERROR HANDLER			
			else:
				print("SORT_BY:Improper sort parameter "+str(root)+"\n")
		return tier

#-------HASHING/ALIAS methods (MD5-compliant)
	
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
	
#-------MULTIPURPOSE methods - largely unrelated to self object
	
	# MODIFIER takes log, creates new category ['jsdt'] for int values returned by get_ms
	def get_jsdt(self):
		for x in self.get_log():
			x['jsdt'] = self.get_ms(x['date'],x['time'])
			x['size'] = 1

	# MODIFIER for exporting - strips ['date'] and ['time'] categories
	def rm_dt(self,hier):
		for x in hier:
			if type(x) is list: # A series of nodes; needs nested call
				x = self.rm_dt(x)
			elif type(x) is dict and 'children' in x: # A node; needs nested call on kids
				x['children'] = self.rm_dt(x['children'])
			elif type(x) is dict: #we are @ base level
				del x['date']
				del x['time']
		return hier 
	
	# SORT HELPER which takes set of data & returns list of (nonrepeat) dates for assembly
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

	# DAY-ENDING CREATOR - for proper labeling, helper to sort function
	def daylabel(self,val):
		if (val % 10 == 1 and val != 11):
			return str(val)+"st"
		elif (val % 10 == 2):
			return str(val)+"nd"
		elif (val % 10 == 3):
			return str(val)+"rd"
		else:
			return str(val)+"th"
	
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
#		return (dtime - datetime.timedelta(hours=4)) # CONVERT from UTC format to boston
		return dtime		

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
		if (message == "secret"):
			data.append((0,0,255)) # top
			data.append((255,0,0)) # bot	
		elif (message == "flip white"):
			data.append((255,255,255))
			data.append((0,0,0))
		elif (message == "flip black"):
			data.append((0,0,0))
			data.append((255,255,255))
		elif (message == "rainbow"):
			data = [(int(128 + 128 * sin(phase)), \
				int(128 + 128 * sin(2.094 + phase)), \
				int(128 + 128 * sin(4.189 + phase))) \
				for phase in [x/1000.0 for x in range(0, 6282, 6282/FIXTURES)]]
			del data[(FIXTURES):] # TRIMS - was @ 75 generated (BRANDON?)
			populate = False
		elif (message.startswith("flip")):
			remainder = message[4:].strip() # chop off flip and strip any spaces
			color = self.look_up_color(remainder)
			inverse = self.complement(color)
			data.append(color)
			data.append(inverse)
		else:
			color = self.look_up_color(message) #rets (x,y,z)(x,y,z)
			data.append(color)
			data.append(color)
		if (populate):	# FORMAT data from 2 RGB tuples to chain of (24*3) numbers  
			data = data * (FIXTURES/2)
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
