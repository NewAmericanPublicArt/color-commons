# Created by Sydney Strzempko(c) for New American Public Art color commons project
# Test file to actually ensure I don't explode things
from fiend import Fiend
from datetime import date, time

d1 = date.today()
d2 = date(2017,1,3)
d3 = date(2017,1,12)
d4 = date(2017,1,23)
d5 = date(2017,2,3)
d6 = date(2017,2,13)
d7 = date(2017,2,23)
d8 = date(2017,3,3)
d9 = date(2017,3,20)
d0 = date(2017,4,6)

t1 = time(22,12)
t2 = time(2,12)
t3 = time(13,52)
t4 = time(8,24)
t5 = time(8,13)
t6 = time(0,58)
t7 = time(13,44)
t8 = time(1,44)
t9 = time(8,24)
t0 = time(23,0)

test = Fiend()
#test.new_entry({'name':'cass','msg':'hi',	'date':d0,	'time':t0})
#test.new_entry({'name':'cass','msg':'hi',       'date':d1,      'time':t1})
#test.new_entry({'name':'cass','msg':'hi',       'date':d2,      'time':t2})
#test.new_entry({'name':'cass','msg':'hi',       'date':d3,      'time':t3})
#test.new_entry({'name':'syd','msg':'bye',       'date':d4,      'time':t4})
#test.new_entry({'name':'cass','msg':'hola',     'date':d5,      'time':t5})
#test.new_entry({'name':'False','msg':'oh no',   'date':d6,      'time':t6})
#test.new_entry({'name':'bevan','msg':'hi',      'date':d7,      'time':t7})
#test.new_entry({'name':'bevan','msg':'hi',      'date':d8,      'time':t8})
test.new_entry({'name':'bevan','msg':'hi',      'date':d9,	'time':t9})
test.new_entry({'name':'bevan','msg':'hi',      'date':d0,	'time':t0})

r1 = time(2,0)
r2 = time(22,0)
empty = {}

alll = test.find(None,empty)
print("all")
for x in alll:
	print(x)

agg1 = test.find(None,{'time':{'start':r1,'end':r2}})
print("Range hr:2-22\n")
for x in agg1:
	print(x)

agg2 = test.find(None,{'name':{'start':"c",'end':"sa"}})
print("Range name:c-sa\n")
for x in agg2:
	print(x)

bymos = test.sort_by("month",test.get_log())
print("Orgz by months")
for x in bymos:
	print(x)



print("end tests")
