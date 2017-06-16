# FILE created by Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of FIEND class for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017

import datetime
import md5

# FIEND CLASS - CONTROLS RPI, ETC FROM LINODE SERVER
class Fiend():
	
	def __init__(self):
            self.log = [] # Empty dict of log entry
	    self.hasher = md5.new() # Establishes multipurpose md5 stream

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

	# Fiend-specific aggregator given particular input fields(groomed input by find())
	def conditional_find(arr,test):
            temp = []
            for x in arr:
            	if ((x['name']==test['name'] or test['name']==False) and
               	    (x['msg']==test['msg'] or test['msg']==False) and
                    (x['date']==test['date'] or test['date']==False) and
	            (x['time']==test['time'] or test['time']==False)):
           	   temp.append(x)
            return temp
     
	# Fiend module which interacts with incomplete/variable-length queries
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
	
	def get_hashable(self,nos):
	    self.hasher.update(str(nos))
	    hex = self.hasher.hexdigest()
	    hex = self.generate_alias(hex)
	    return hex	   
	    # TO RETURN - a silly name like "Mr. Vernon" of type STR
	
	def generate_alias(self,hash):
	    # TODO - THIS FUNCTION CROSS-REFERENCES W 2 LISTS ND LAST 4 DIGS
	    key = hash
	    return "Capt. Bev"	

	def get_time(self):
	   return datetime.datetime.time(datetime.datetime.now()) # TODO - incorporate tzinfo, convert format
	
	def get_date(self):
	   return datetime.date.today() # DATE hardwired naive; TODO convert format
