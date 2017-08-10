# (c) Sydney Strzempko for NAPA Color Commons 2017
# File generating GREENWAY data request values
from fiend import Fiend
import datetime

sampler = Fiend( [], None )
sampler.get_fr_csv('current.csv')

q = {'date':{'start': datetime.date(2017,7,11), 'end': datetime.date(2017,7,25)}}

print("1) Number of unique users during this time")

arg1 = ["range", datetime.date(2017,7,11), datetime.date(2017,7,25), "user"]
print(len((sampler.load(None,arg1))['children'])) # Length of # of unique users in span

print("2) Number of total texts to the CC up to the end of this period")
print(len(sampler.find(None,{'date':{'start':datetime.date(2017,1,1),'end':datetime.date(2017,7,25)}})))

print("3) Number of NEW users during this period")
print(len(sampler.sort_by("newuser", sampler.find( None, q))))

print("4) Number of Unique Users for the WHOLE project")
print(len(sampler.sort_by("user", sampler.get_log() )))



