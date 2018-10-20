import datetime
s = datetime.datetime.now()


s = str(s).split(".")[0]
print(s,type(s))