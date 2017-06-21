# TEST INPUT FOR HASH FUNCTION present in fiend.py
# Sydney Strzempko (c) for New American Public Art

from fiend import Fiend # should have NAMES/SURS imported as well

bubba = Fiend()

nos = ["+15888104523","+14888623807","+15088883887","+99999999999"]

x = bubba.get_hashable(nos[0])
y = bubba.get_hashable(nos[1])
z = bubba.get_hashable(nos[2])
xtra = bubba.get_hashable(nos[3])

print("A is "+x)
print("B is "+y)
print("C is "+z)
print("D is "+xtra)
print("*********END tests")
