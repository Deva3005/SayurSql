from datetime import datetime,timedelta
import random
x=datetime.strptime("2025-09-15","%Y-%m-%d")
print(x)
sales=[]
for i in range(75):
    # booki, customerid, qty,sales date
    temp=(random.randrange(1,55),random.randrange(1,6),random.randrange(5,21),x.strftime("%Y-%m-%d"))
    sales.append(temp)
    print(x)
    x+=timedelta(1)