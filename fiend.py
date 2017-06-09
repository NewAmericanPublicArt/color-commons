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
    def log_csv(self,filex):
        return filex
        # Loads SEVERAL entries from preexisting/compiled fr Twilio
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
    def to_csv(self):
        return filex
                # Not sure if needed

# TODO - transition over more from server.py into this

# Sanitize function - uses encode & decode modules of strings
# Suggestion from Vasily Alexeev
# https://stackoverflow.com/questions/8689795/how-can-i-remove-non-ascii-characters-but-leave-periods-and-spaces-using-python#comment72965907_18430817
def sanitize(input):
    return input.decode('utf-8').encode('ascii',errors='ignore')