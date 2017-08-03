from fiend import Fiend
from datetime import date

app = Fiend()

# TODAY
app.new_entry({'name':"+6094776026",'msg':"purple"})
app.new_entry({'name':"+5083000678",'msg':"crimson"})
app.new_entry({'name':"+4006778796",'msg':"yellow"})
# PAST
app.new_entry2({'name':"+0000000000",'msg':"blue",'date':date(2015,3,23)})
app.new_entry2({'name':"+6094776026",'msg':"red",'date':date(2013,4,26)})
app.new_entry2({'name':"+0000000000",'msg':"pruple",'date':date(2014,6,15)})
app.new_entry2({'name':"+4006778796",'msg':"green",'date':date(2015,8,21)})
app.new_entry2({'name':"+2334564563",'msg':"blue",'date':date(2015,8,4)})
app.new_entry2({'name':"+1111111111",'msg':"maroon",'date':date(2016,10,26)})

# arr0 = app.find(None,None)
# for i in arr0:
#	print(i['name'])
#print("   ")

arr0 = app.find(None,{'date':{'start':date(2015,8,1), 'end':date(2015,9,1)}})
for i in arr0:
	print(str(i['name'])+str(i['date']))


arr = app.find(None,{'date':{'start':date(2017,7,1),'end':date(2017,7,8)}})
for i in arr:
	print(i['name'])

print("   ")

arr2 = app.sort_by("newuser",arr)
for i in arr2:
	print(i)
