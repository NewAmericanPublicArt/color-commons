from fiend import Fiend

app = Fiend([],None)
app.get_fr_csv('current.csv') # For import

print(str(app.sort_by("month",app.get_log()))[:200])
print("                     ")
print(str(app.sort_by("day",app.get_log()))[:200])
print("                     ")
print(str(app.sort_by("hour",app.get_log()))[:200])
print("                     ")
print(str(app.sort_by("users",app.get_log()))[:200])
print("                     ")
print(str(app.sort_by("newuser",app.get_log()))[:200])

