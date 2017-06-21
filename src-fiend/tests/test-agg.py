# Created by Sydney Strzempko(c) for New American Public Art color commons project
# Test file to actually ensure I don't explode things
from fiend import Fiend

test = Fiend()
test.new_entry({'name':'cass','msg':'hi','stamp':15})
test.new_entry({'name':'syd','msg':'bye','stamp':5})
test.new_entry({'name':'cass','msg':'hola','stamp':32})
test.new_entry({'name':'False','msg':'oh no','stamp':100})
test.new_entry({'name':'bevan','msg':'hi','stamp':15})

empty = {}

alll = test.find(empty)
casses = test.find({'name':'cass'})
his = test.find({'msg':'hi'})
agg_2 = test.find({'msg':'hi','stamp':15})

test.new_entry({'name':'cass','msg':'hi','stamp':15})
agg_3 = test.find({'name':'cass','msg':'hi','stamp':15})

# THEN PRINT THEM TO CHECK
print("all")
for x in alll:
	print(x)
print("casses")
for x in casses:
	print(x)
print("his")
for x in his:
	print(x)
print("agg hi 15")
for x in agg_2:
	print(x)
print("agg cass hi stamp")
for x in agg_3:
	print(x)

print("end tests")