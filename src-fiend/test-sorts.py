from fiend import Fiend
from datetime import date,time

app = Fiend([],None)

# TODAY
app.new_entry({'name':"+1111111111",'msg':"purple"})
app.new_entry({'name':"+2222222222",'msg':"crimson"})
app.new_entry({'name':"+3333333333",'msg':"yellow"})
app.new_entry({'name':"+1111111110",'msg':"purple"})
# PAST
app.new_entry2({'name':"+0000000000",'msg':"blue",'date':date(2015,3,23),'time':time(15,0,0)})
app.new_entry2({'name':"+1111111111",'msg':"red",'date':date(2013,4,26),'time':time(15,0,0)})
app.new_entry2({'name':"+0000000000",'msg':"pruple",'date':date(2014,6,15),'time':time(15,0,0)})
app.new_entry2({'name':"+2222222222",'msg':"green",'date':date(2015,8,21), 'time':time(15,0,0)})
app.new_entry2({'name':"+3333333333",'msg':"blue",'date':date(2015,8,4), 'time':time(15,0,0)})
app.new_entry2({'name':"+1111111111",'msg':"maroon",'date':date(2016,10,26), 'time':time(15,0,0)})

print("ALL before 8/1")
arr = app.find(None,{'date':{'start':date(2013,1,1),'end':date(2017,8,1)}})
for i in arr:
    print(i)

print("UU before 8/1")
sarr = app.sort_by("user", arr)
for i in sarr:
    print(i)  

print("ALL after 2017")
arr0 = app.find(None,{'date':{'start':date(2017,1,1), 'end':date(2017,10,10)}})
for i in arr0:
    print(i)

print("UU after 2017")
sarr1 = app.sort_by("user", arr0)
for i in sarr1:
    print(i)  

print("NEW after 2017")
arr2 = app.sort_by("newuser",sarr1)
for i in arr2:
    print(i)
