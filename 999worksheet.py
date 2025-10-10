import mysql.connector
import random
from functools import reduce
from tabulate import tabulate

class BookStoreDB:

    db=mysql.connector.connect(
           host="localhost",
           user="deva",
           password="deva",
           database="BookStore_remastered"
       )
    
    cursor=db.cursor()
    def insert_data_books(self):
        
        list_book=[(f"Vol {x} Master & Slaves","Deva",random.randrange(200,1000),random.randrange(1,30)) for x in range(1,50)]
        books=[
        ("Ponniyin Selvan", "Kalki", 399.0, 10),
        ("Thirukkural", "Thiruvalluvar", 199.0, 3),
        ("Wings of Fire", "A.P.J. Abdul Kalam", 350.0, 7),
        ("The Alchemist", "Paulo Coelho", 299.0, 2),
        ("The Guide", "R.K. Narayan", 250.0, 8)
    ]
        self.cursor.executemany("insert into Books(Title,Author,Price,Quantity) values(%s,%s,%s,%s)",list_book)
        self.db.commit()
    
    def insert_data_customer_and_sales(self):
        customers = [
        (1, "Arjun", "arjun@example.com", "Chennai"),
        (2, "Priya", "priya@example.com", "Coimbatore"),
        (3, "Ravi", "ravi@example.com", "Madurai")
]
        sales = [
    (1, 1, 1, 2, "2025-09-10"),  # Arjun buys 2 Ponniyin Selvan
    (2, 3, 2, 1, "2025-09-11"),  # Priya buys 1 Wings of Fire
    (3, 2, 3, 1, "2025-09-12")   # Ravi buys 1 Thirukkural
]

        self.cursor.executemany("insert into Customers values(%s,%s,%s,%s)",customers)
        self.db.commit()

        self.cursor.executemany("insert into Sales values(%s,%s,%s,%s,%s)",sales)
        self.db.commit()



    def show_all_books(self):
        self.cursor.execute("select * from Books")
        return self.cursor.fetchall()
    
    def show_books_schema(self):
        self.cursor.execute("DESCRIBE Books;")
        return self.cursor.fetchall()
    def run(self):
        self.cursor.execute("""
select quantity from Books where Title='A and Author = {Author}""")
    def list_emails(self):
        self.cursor.execute("select email from Customers;")
        return reduce(lambda x,y:x+y,self.cursor.fetchall())
    
    # Get customer Details via Email
    def get_customer_details(self,email):
        self.cursor.execute(f"select * from Customers where email = '{email}'")
        return self.cursor.fetchall()[0]
    
    def get_customer_details1(self,email):
        self.cursor.execute(f"select * from Customers where email = '{email}'")
        return [x for i in self.cursor.fetchall() for x in i]
    
    # Listing Schema for Update and Create Purposes [User Management] [*]
    def show_customer_schema(self):
        self.cursor.execute("DESCRIBE Customers;")
        return self.cursor.fetchall()

# db=BookStoreDB()
# x=db.get_customer_details1("arjun@example.com")
# print(x)

# books=[
#         ("Ponniyin Selvan", "Kalki", 399.0, 10),
#         ("Thirukkural", "Thiruvalluvar", 199.0, 3),
#         ("Wings of Fire", "A.P.J. Abdul Kalam", 350.0, 7),
#         ("The Alchemist", "Paulo Coelho", 299.0, 2),
#         ("The Guide", "R.K. Narayan", 250.0, 8)
#     ]
# print([x[0] for x in books])

# Carting and Checkout with stock update... [List Not worked well]
# import pyinputplus as pyinp
# cart=[]
# stock_of_book=10
# while True:
#     customerId=1
#     bookId = input("Book Id")
#     print(stock_of_book, "Stock Is available")
#     quantity = pyinp.inputInt(prompt="Kindly enter the Quantity...\t",min=1,max=stock_of_book)
#     # Sales Table Entity
#     if cart:
#         for item in cart:
#             print(item)
#             if bookId == item[0]:
#                 print("Purchase already maded")
#                 continue
#         # else:
#         #     x=[bookId,customerId,quantity]
#         #     cart.append(x)
#     else:
#         x=[bookId,customerId,quantity]
#         cart.append(x)
#     print(cart)

# Tuple is immutable so can't change the value 
# so tuple to list
# x=[1,2,3]
# x[0]="deva"
# print(x)


a={1:["deva","today"],2:["arjun","afternoon"]}
sales=[[x]+a[x] for x in a]
print(sales)



# CENTER and FORMAT console output
# ---------------------------------+
# import shutil
# import os
# books=[
#         ("Ponniyin Selvan xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "Kalki", 399.0, 10),
#         ("Thirukkural", "Thiruvalluvar", 199.0, 3),
#         ("Wings of Fire", "A.P.J. Abdul Kalam", 350.0, 7),
#         ("The Alchemist", "Paulo Coelho", 299.0, 2),
#         ("The Guide", "R.K. Narayan", 250.0, 8)
#     ]
# print("Deva".center(shutil.get_terminal_size().columns,"*"))
# print(shutil.get_terminal_size().columns)
# for i in tabulate(books).splitlines():
#     print(i.center(shutil.get_terminal_size().columns-50," "))


# Nested Class TryOUT

# class a:
#     x=None
#     def __init__(self):
#         print("A Class")
#         self.x=self.b()
#         print(self.x.name)
#     # Nested Class
#     class b:
#         name="b name variable..."
# a=a()
# # c=a.b()
# # print(c.name)

