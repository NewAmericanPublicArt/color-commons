from fiend import Fiend
import datetime

app = Fiend()

app.get_fr_csv('6-7forward.csv')

for val in app.get_log():
    print(app.get_ms(val['date'],val['time']))

print("done")
