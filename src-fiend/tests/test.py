from fiend import Fiend
from datetime import date,time

app = Fiend([],None)
app.get_fr_csv('current.csv')

found = app.find(None,{'date':date(2017,7,25)})
found2 = app.find(None,{'msg':'Shatt'})

for i in found:
    print(i)
for i in found2:
    print(i)
