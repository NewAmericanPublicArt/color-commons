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
test.new_entry({'name':'cass','msg':'hi',	'date':d0,	'time':t0})
test.new_entry({'name':'cass','msg':'hi',       'date':d1,      'time':t1})
test.new_entry({'name':'cass','msg':'hi',       'date':d2,      'time':t2})
test.new_entry({'name':'cass','msg':'hi',       'date':d3,      'time':t3})
test.new_entry({'name':'syd','msg':'bye',       'date':d4,      'time':t4})
test.new_entry({'name':'cass','msg':'hola',     'date':d5,      'time':t5})
test.new_entry({'name':'False','msg':'oh no',   'date':d6,      'time':t6})
test.new_entry({'name':'bevan','msg':'hi',      'date':d7,      'time':t7})
test.new_entry({'name':'bevan','msg':'hi',      'date':d8,      'time':t8})
test.new_entry({'name':'bevan','msg':'hi',      'date':d9,	'time':t9})
test.new_entry({'name':'bevan','msg':'hi',      'date':d0,	'time':t0})

empty = {}

alll = test.find(empty)
casses = test.find({'name':'cass'})
his = test.find({'msg':'hi'})
agg = test.find({'msg':'hi','time':t0})

r1 = time(2,0)
r2 = time(22,0)
agg1 = test.find({'time':{'start':r1,'end':r2}})


# THEN PRINT THEM TO CHECK
print("all")
for x in alll:
	print(x)
print("casses")
for x in casses:
	print(x)
print("hi-s")
for x in his:
	print(x)
print("agg: hi 8:24")
for x in agg:
	print(x)
print("range: TIME from 2:00 to 22:00")
for 



print("end tests")
