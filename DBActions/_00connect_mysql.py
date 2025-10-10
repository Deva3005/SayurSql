from functools import reduce
import time
import mysql.connector
import pyinputplus as pyinp

class BookStoreDB:
    # Connection to the Database
    db=mysql.connector.connect(
           host="localhost",
           user="deva",
           password="deva",
           database="BookStore_remastered"
       )
    
    # Cursor Attribute 
    cursor=db.cursor()

    # Listing all Books and return List [Catalogue] [1]
    def show_all_books(self,offset:int)->list:
        # Pagination
        self.cursor.execute(f"select * from Books limit 10 offset {offset}")
        return self.cursor.fetchall()
    
    # Total Count of Books for PAGINATION [Catalogue] [1]
    def total_books_entries(self)->int:
        self.cursor.execute("select count(*) from Books;")
        return self.cursor.fetchone()[0]
    
    # Search and Filter
    def show_search_results(self,offset:int,title:str)->list:
        self.cursor.execute(f"select * from Books where title like '%{title}%' limit 10 offset {offset}")
        return self.cursor.fetchall()
    
    # Total Count of Books for PAGINATION [search] [Catalogue] [1]
    def total_search_result(self,title)->int:
        self.cursor.execute(f"select count(*) from Books where title like '%{title}%'")
        return self.cursor.fetchone()[0]
    
    # Listing Schema for Update and Create Purposes [BookManagement] [2]
    def show_books_schema(self):
        self.cursor.execute("DESCRIBE Books;")
        return self.cursor.fetchall()
    
    # Create Book Dictionary >> Input for New Book Entry skipped Id [BookManagement] [2]
    def create_book(self):
        book={
        }
        for table_data in self.show_books_schema()[1:]:
            book.setdefault(table_data[0],input(f"Enter the {table_data[0]}..."))
        return book
    
    # Create Book Dictionary >> Input for Update Book Qty skipped Id & Price [BookManagement] [2]
    def create_update_book(self):
        book={
        }
        for table_data in self.show_books_schema()[1:]: # From schema dict key is prepared.
            if table_data[0] == 'price':
                continue
            book.setdefault(table_data[0],input(f"Enter the {table_data[0]}..."))
        return book
    
    # Cursor - Insert Execution & Update [Commit action] [BookManagement] [2]
    def add_books_to_table(self,title:str,author:str,price:float,quantity:int):
        # INSERT ACTION
        self.cursor.execute("""
                            insert into 
                            Books (Title,Author,Price,Quantity) 
                            values (%s,%s,%s,%s)""",
                            (title,author,price,quantity))
        # COMMIT ACTION
        self.db.commit()
        print(f"{title} Books is updated in the Table...")
    
    # Cursor - Update Execution & Update [Commit action] [BookManagement] [2]
    def update_book_quantity_on_re_stocking(self,title,author,quantity):
        # UPDATE ACTION
        self.cursor.execute(f"""
                            update Books 
                            set 
                            quantity={quantity}+quantity
                            where Title like '%{title}%' and Author = '{author}'""")
        # COMMIT ACTION
        self.db.commit()
        print(f"{title} books quantity is updated")
    
    # List All Emails
    def list_emails(self):
        self.cursor.execute("select email from Customers;")
        return reduce(lambda x,y:x+y,self.cursor.fetchall())
    
    # Get customer Details via Email
    def get_customer_details(self,email):
        self.cursor.execute(f"select * from Customers where email = '{email}'")
        return [x for i in self.cursor.fetchall() for x in i]
    
    # Listing Schema for Update and Create Purposes [User Management] [*]
    def show_customer_schema(self):
        self.cursor.execute("DESCRIBE Customers;")
        return self.cursor.fetchall()
    
    # Create Book Dictionary >> Input for New Book Entry skipped Id [BookManagement] [2]
    def create_customer(self):
        customer={
        }
        for table_data in self.show_customer_schema()[1:]:
            if (table_data[0]=="email"):
                customer.setdefault(table_data[0],pyinp.inputEmail(f"Enter the {table_data[0]}...\t"))
            else:
                customer.setdefault(table_data[0],input(f"Enter the {table_data[0]}...\t"))
        return customer
    
    # Cursor - Insert Execution & Update [Commit action] [UserManagement] [*]
    def add_customer_to_table(self,name:str,email:str,city:str):
        # INSERT ACTION
        self.cursor.execute("""
                            insert into 
                            Customers (name,email,city) 
                            values (%s,%s,%s)""",
                            (name,email,city))
        # COMMIT ACTION
        self.db.commit()
        print(f"Customer {name} is Registered Successfully")
        time.sleep(2)
    
    # Check Stock for Book Id
    def check_stock(self,bookId):
        self.cursor.execute(f"""
            select quantity from Books where id = {bookId}
        """)
        return self.cursor.fetchone()
    
    # Cursor - Update Execution & Update [Commit action] [Purchase Management] [3]
    def update_book_quantity_on_purchase(self,bookId,quantity):
        self.cursor.execute(f"""
                            update Books 
                            set 
                            quantity={quantity}-quantity
                            where id='{bookId}'""")
        self.db.commit()

    # Sales Table Insert | Entry
    def update_sales_data(self,sales_data:list):
        self.cursor.executemany("""
                INSERT INTO `Sales` (bookid,customerid,quantity_sold,sales_date) VALUES (%s,%s,%s,%s)
        """,sales_data)
        self.db.commit()