# TESTER FOR CSV FILE INPUT
# Sydney Strzempko (c) for New American Public Art Color Commons project
from fiend import Fiend
import datetime

app = Fiend()

app.get_fr_csv('test.csv')

list = app.get_log()

for i in list:
	print(i['name'])

