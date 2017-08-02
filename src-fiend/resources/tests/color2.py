# SAMPLE FILE for running a standard colorish sort given extant log

from fiend import Fiend
from datetime import date, time

###############################################################################

app = Fiend([],None)	#init format; Fiend( log, hash ); So [], None as standard values
app.get_fr_csv('current.csv') #brings in all old values from csv (given path)

early_jun_query = {'date': {'start':date(2017,7,1), 'end':date(2017,7,8)} }

early_jun_data = app.find( None, early_jun_query ) #format; find( source, query )
						   # When source = None, defaults to log

sorted_tree = app.sort_by( "color2", early_jun_data ) #format; sort_by( phrase, source )
						   # When None, does NOT default to log
for x in sorted_tree:
    print(x)

