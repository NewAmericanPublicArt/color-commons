from fiend import Fiend
from datetime import date

app = Fiend()

app.new_entry({'name':"+6094776026",'msg':"purple"})
app.new_entry({'name':"+5083000678",'msg':"crimson"})
app.new_entry({'name':"+4006778796",'msg':"yellow"})


app.new_entry2({'name':"+0000000000",'msg':"blue",'date':date(2015,3,23)})
app.new_entry2({'name':"+6094776026",'msg':"red",'date':date(2013,4,26)})
app.new_entry2({'name':"+0000000000",'msg':"pruple",'date':date(2014,6,15)})
app.new_entry2({'name':"+4006778796",'msg':"green",'date':date(2015,8,21)})
app.new_entry2({'name':"+1111111111",'msg':"maroon",'date':date(2016,10,26)})

arr = app.find(app.get_log(),{'date':{'start':date(2017,6,20),'end':date.today()}})

arr2 = app.sort_by("newuser",arr)

print("Newusers before last week\n")
for i in arr2:
	print(i)

