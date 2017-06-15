# FILE created by Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of FIEND class for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017

# Fiend-specific aggregator given particular input fields
def conditional_find(arr,test):
        temp = []
        for x in arr:
                if ((x['name']==test['name'] or test['name']==False) and
                    (x['msg']==test['msg'] or test['msg']==False) and
                    (x['stamp']==test['stamp'] or test['stamp']==False)):
                        temp.append(x)
        return temp

# FIEND CLASS - CONTROLS RPI, ETC FROM LINODE SERVER
class Fiend():
        
	def __init__(self):
                self.log = [] # Empty dict of log entry
	
	def new_entry(self,elem):
            # Elem should be of type {'name':'x','msg':'y','stamp':'z'}
            if not(elem and ('name' in elem) and ('msg' in elem) and ('stamp' in elem)):
                print("improper entry format")
                return False
            self.log.append(elem)
            return True
	
	def find(self,entry):
	    found = []
	    if query: #Essentially generates placeholders for cond_find
                if 'name' not in query:
             	   query['name'] = False
                if 'msg' not in query:
                   query['msg'] = False
                if 'stamp' not in query:
                   query['stamp'] = False
                found = conditional_find(self.log,query)
            return found # if !query, returns empty list
