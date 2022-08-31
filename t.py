    
from datetime import date, datetime



allglist = '2022-10-10'
cdata=()
l1=[]
today = date.today()

# fdate = i.expirydate
y =int(allglist[0:4])
m = int(allglist[5:7])
d =int(allglist[8:10])
print(y,m,d)
# y,m,d = 2022,10,10

future = date(y,m,d)
diff = future - today
print (diff.days)
days = diff.days
# cdata=()
# cdata=(days)
# l1.append(cdata)
# print(l1)