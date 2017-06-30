# Created by Sydney Strzempko(c) for New American Public Art color commons project
# Test file to actually ensure I don't explode things
from fiend import Fiend
from datetime import date, time

d = [date.today(),date(2017,6,3),date(2017,4,12),date(2017,1,23),date(2016,12,3),date(2016,10,13),date(2016,8,23),date(2016,6,3),date(2016,3,20),date(2015,4,6)]
t = [time(0,12),time(2,12),time(3,52),time(5,24),time(8,13),time(12,58),time(13,44),time(16,44),time(18,24),time(23,0)]
x = Fiend()

x.new_entry({'name':'+0000000011','msg':'red'})
x.new_entry({'name':'+0000003333','msg':'redorange'})
x.new_entry({'name':'+0000034567','msg':'orange'})
x.new_entry({'name':'+0000345678','msg':'peach'})
x.new_entry({'name':'+0004567890','msg':'chartreuse'})
x.new_entry({'name':'+0001112345','msg':'green'})
x.new_entry({'name':'+0002223456','msg':'blue'})
x.new_entry({'name':'+0003334567','msg':'violet'})
x.new_entry({'name':'+0003334567','msg':'purple'})
x.new_entry({'name':'+0034567890','msg':'orange'})
x.new_entry({'name':'+0234567890','msg':'flip black'})

r1 = time(18,13,0)
r2 = time(18,13,47)
empty = {}

alll = x.find(None,empty)
print("all\n")
for i in alll:
	print(i)

agg1 = x.find(None,{'time':{'start':r1,'end':r2}})
print("Range first 1/2 hr\n")
for i in agg1:
	print(i)

agg2 = x.find(None,{'name':{'start':"A",'end':"M"}})
print("Range names A-M\n")
for i in agg2:
	print(i)

bymos = x.sort_by("month",x.get_log())
print("Orgz by months\n")
for i in bymos:
	print(i)

aggfinal = x.find(None,{'msg':{'start':"cold",'end':"red"}})
print("Bw RED and COLD\n")
for i in aggfinal:
	print(i)

print("*************end tests")
