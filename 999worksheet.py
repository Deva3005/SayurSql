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

    def get_book_details(self,bookid):
        self.cursor.execute(f"select * from Books where id = {bookid}")
        return self.cursor.fetchall()

    def gen_book_detail_for_bill(self,bookid)->list:
        det=self.get_book_details(bookid)
        # 0 -> Title
        # 1 -> Author
        # 2 -> Price
        # 3 -> Qty
        # ("Ponniyin Selvan", "Kalki", 399.0, 10)
        return [x for x in det]

    def get_purchase_details(self,offset=None):
        query="""
            SELECT s.sales_date,b.title,b.author,b.price,s.quantity_sold,c.name,c.email,c.city
            from `Sales` as s 
            JOIN `Books` as b 
                on s.bookid = b.id
            JOIN `Customers` as c
                on s.customerid = c.id
        """
        if offset==None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query+f"limit 10 offset {offset}")
        return self.cursor.fetchall()

    def total_purchase_count(self):
        self.cursor.execute("select count(*) from Sales")
        return self.cursor.fetchall()

    def get_purchase_det_by_user(self,offset,id):
        list_attr="""
                SELECT
                    s.sales_date,
                    c.name,
                    -- c.email,
                    c.city,
                    -- s.bookid,
                    b.title,
                    CONCAT("x ",s.quantity_sold),
                    CONCAT("$ ",b.price),
                    CONCAT("$ ",b.price*s.quantity_sold) as total """
        count="""select count(*) """
        query=f"""
            from `Customers` as c
            LEFT JOIN `Sales` as s ON c.id=s.customerid
            LEFT JOIN `Books` as b on b.id=s.bookid
            -- GROUP BY city
            where c.id={id}
            ORDER BY s.sales_date desc """
        self.cursor.execute(list_attr+query+f"\nlimit 10 offset {offset}")
        l=self.cursor.fetchall()
        self.cursor.execute(count+query)
        c=self.cursor.fetchall()[0]
        return l,c
    
    def test_most_valuble_records_data(self):
        print("testing....")
        self.cursor.execute("""
            SELECT 
        -- c.id,c.name,c.email,
        c.city,
        -- s.sales_date,s.bookid,
        sum(s.quantity_sold),
        -- b.title,b.price,
        sum(b.price*s.quantity_sold) as total 
    from `Customers` as c
    LEFT JOIN `Sales` as s ON c.id=s.customerid
    LEFT JOIN `Books` as b on b.id=s.bookid
    GROUP BY city
    ORDER BY total desc; 
        """)
    
        return self.cursor.fetchall()

db=BookStoreDB()
# x=db.test_most_valuble_records_data()
# print(x)
# print(tabulate(x,tablefmt="grid"))
# print(y)

print("""
              
        ,....,
      ,::::::<              Most Valuable Customer of Bookstore 101 || {datetime.now().strftime("%Y")} ||
     ,::/^\"``.
    ,::/, `   e`.           Name            : {data[1]}
   ,::; |        '.
   ,::|  \___,-.  c)        Email           : {data[2]}
   ;::|     \   '-'
   ;::|      \              Location        : {data[3]}
   ;::|   _.=`\


        Home  [0]

        """)

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


# a={1:["deva","today"],2:["arjun","afternoon"]}
# sales=[[x]+a[x] for x in a]
# print(sales)



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

