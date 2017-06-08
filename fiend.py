# File created by Sydney Strzempko(c) for NEW AMERICAN PUBLIC ART association
# Implementation of FIEND class for use in server of color commons project
# Link: http://www.newamericanpublicart.com/color-commons-2017

# See how nasty this is? Trying to separate from declaration
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
                # Do here
                self.log = [] # Empty dict of log entries
        def log_csv(self,file):
                # Loads SEVERAL entries from preexisting/compiled fr Twilio
        def new_entry(self,elem):
                # Elem should be of type {'name':'x','msg':'y','stamp':'z'}
                if !(elem and elem['name'] and elem['msg'] and elem['stamp']):
                        print("improper entry format")
                        return False
                elem = sanitize(elem)
                self.log.append(elem)
                return True
        def find(self,query): # Returns a list of terms matching query
                found = []
                if query: #Essentially generates placeholders for cond_find
                        if !query['name']:
                                query['name'] = False
                        if !query['msg']:
                                query['msg'] = False
                        if !query['stamp']:
                                query['stamp'] = False
                        found = conditional_find(self.log,query)
                return found #if !query, returns empty list
        def to_csv(self):
                # Not sure if needed

# TODO Add class Log():?

# TODO - transition over more from server.py into this







