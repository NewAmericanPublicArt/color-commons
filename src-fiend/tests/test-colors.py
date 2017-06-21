# TEST FILE FOR NEW COLOR PARSING FUNCTIONALITY
# Sydney Strzempko (c) 2017 for New American Public Art

from fiend import Fiend

girl = Fiend()

msg = ["secret","flip white","flip black","flip red","rainbow","green","purple","black"]

for x in msg:
	temp = girl.parse_command(x)
	print("***TESTING FOR INPUT:\n")
	print(x)
	print(temp)
	print(len(temp))
	print("\n***\n")

print("***TESTING COMPLETE")
