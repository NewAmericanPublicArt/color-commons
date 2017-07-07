# Sydney Strzempko (c) 2017 for New American Public Art Color Commons
#
# FILE TO GENERATE NEEDED INFORMATION FOR MBTA PEOPLE
# WILL SPIT OUT RELEVANT INFORMATION INTO "GWAY.MD"
#
# NOTE: Modified .csv file from Twilio download in order to gain latest info in realtime.
#	In the future, with fiend installed this import will be useless
#	as Fiend will catch all incoming messages
#	However, in order to ensure that our .csv would be parsed correctly, we took the
#	original and converted out line breaks (in current.csv)
#	Although this fell out of the scope of our Fiend program's functionality, due to
#	the above explanation the method by which this was performed (grep sed) will be omitted.
#	Ideally, this won't be an issue in the future.
#
#	Input:	current.csv
#	Output: GWAY.md
#
#	Dates can be changed at any time by modifying the "requested" object following format
#
import csv
from datetime import date, time
from fiend import Fiend

app = Fiend() # Inits instance of our monster

app.get_fr_csv('current.csv') # Loads with information

requested = [
	["Feb 14th-28th",date(2017,2,14),date(2017,2,28)],
	["Apr 11th-25th",date(2017,4,11),date(2017,4,25)],
	["May 3rd-17th",date(2017,5,3),date(2017,5,9)]]

week1 = [app.find(None,{'date':{'start':requested[0][1],'end':requested[0][2]}}),requested[0][0]] # First week chunk
week2 = [app.find(None,{'date':{'start':requested[1][1],'end':requested[1][2]}}),requested[1][0]] # 2nd week chunk
week3 = [app.find(None,{'date':{'start':requested[2][1],'end':requested[2][2]}}),requested[2][0]] # 3rd week chunk
weeks = [week1, week2, week3]

for i in weeks:
    print(i[1])	
    print(i[0])

file = open("GWAY.md",'w')
file.write("# Stats for the Color Commons\n")
file.write("generated by NAPA for the Rose Kennedy Greenway Color Commons Project\n")
file.write("### Link\n")
file.write("[NAPA](http://www.newamericanpublicart.com/color-commons-2017)\n")

for week in weeks:
    total_texts = len(week[0])
    unique_users = app.sort_by("users",week[0])
    new_users = app.sort_by("newuser",week[0])

    print("unique users")
    print(unique_users)	
    print("new_users")
    print(new_users)	

    file.write("## FOR THE WEEK OF:\n")
    file.write(week[1]+'\n')
    file.write("# Total texts\n")
    file.write(str(total_texts))
    file.write("\n# Unique users\n")
    file.write(str(unique_users))
    file.write("\n# New/Firsttime users\n")
    file.write(str(new_users))
    file.write("\n------\n")

file.close()
