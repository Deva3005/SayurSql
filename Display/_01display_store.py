import time
from DBActions._00connect_mysql import *
import os
import pyinputplus as pyinp
from datetime import datetime
from tabulate import tabulate
import shutil

class DisplayStore:

    db=BookStoreDB()

    customerName="Anonymous"
    customerEmail="No Email for Anonymous!!!"
    customerid=f"[+]"
    datenow=datetime.now().strftime("%Y-%m-%d")
    # list_of_purchase=[] # List is not worked well for carting and checkout
    list_of_purchase=dict()
    customerDetails=None

    def display_header(self):
        self.clear_screen()
        header=f"""

                            Welcome to BookStore 101


        
    user  = {self.customerName}|{self.customerid}                        Date = {self.datenow}
    email = {self.customerEmail}
    


                                __..._   _...__
                            _..-"      `Y`      "-._
                            \ Once upon |           /
                            \\  a time..|          //
                            \\\         |         ///
                             \\\ _..---.|.---.._ ///
                              \\`_..---.Y.---.._`//
                                '`               `'

        
        """
        return header

    #+++++Miscellaneous+++++++++++++++++++++++++++++++++++++

    # Miscellaneous Clear Screen!!!
    def clear_screen(self):
        os.system("cls")

    # Miscellaneous Home Screen!!!
    def display_home(self):
        self.clear_screen()
        print(self.display_header()+"""
              
              ++++++++++++++   HOME         ++++++++++++++
              
              [1] Login/Register.......................[ok]
              [2] Catalogue............................[ok]
              [3] Book Management......................[ok]
              [4] Purchase Management..................[ok]
              [5] Review All Purchase..................[ok]
              [6] Customer Management..................[ok]
              [7] MOST VALUBLE RECORDS.................[ok]
              [q] Quit.................................[ok]

            """)

    # Miscellaneous Error Screen!!!
    def display_unauthorized(self):
        self.clear_screen()
        print(self.display_header()+"""

            UN-AUTHORIZED | PROHIBITED
              
            Press any Key to reach HOME Page [0]
            """)
        input()
        self.display_home()
    
    #+++++Catalogue++++++++++++++++++++++++++++++++++++++

    #[1] Catalogue............................[ok]
    def display_all_books(self,offset=0):
        # Clearing Terminal
        self.clear_screen()

        # From DB actions -> List of Books
        Books=self.db.show_all_books(offset) # Limits 10

        print(self.display_header())

        # print(tabulate(Books,headers=["Book ID","Title","Author","Price","Stock"],tablefmt="grid"))

        # Formatting the Outputs
        for book in Books:
            for detail in book:
                if type(detail)==str:
                    if len(detail)>=len("Brothers of Shadows Sleep"):
                        detail=detail[:len("Brothers of Shadows.....")]+"..."
                    print(detail.ljust(len("Brothers of Shadows Sleep")," "),end="\t")
                else:
                    print(detail,end="\t")
            print()

        print("""

        Previous [p]                                       Next  [n]
              
        Home     [0]                                     Search  [s]
        
        """)
        # Exit Navigation to Home
        x=input("Enter Input ::: \t")
        if x=='0' or x=='o':
            self.display_home()
        elif x=="n":
            offset+=10
            if offset >= self.db.total_books_entries():
                offset = self.db.total_books_entries()-10
                self.display_all_books(offset)
            else:
                self.display_all_books(offset)
        elif x=="p":
            offset-=10
            if offset<=0:
                offset=0
                self.display_all_books(offset)
            else:
                self.display_all_books(offset)
        elif x=="s":
            title=input("Enter the Book Title Keyword......For Search\t")
            self.display_searched_books(title=title,offset=0)
        else:
            self.display_unauthorized()

    #[1] Catalogue Search ............................[ok]

    def display_searched_books(self,title,offset):
        total=self.db.total_search_result(title)
        # Clearing Terminal
        self.clear_screen()
        print(self.display_header()+f"""
              
        Search Results of {title} Key >>> Total Results = {total}

        """)
        # From DB actions -> List of Books
        Books=self.db.show_search_results(title=title,offset=offset) # Limits 10
        print("Offset",offset)
        # Formatting the Outputs
        for book in Books:
            for detail in book:
                if type(detail)==str:
                    if len(detail)>=len("Brothers of Shadows Sleep"):
                        detail=detail[:len("Brothers of Shadows.....")]+"..."
                    print(detail.ljust(len("Brothers of Shadows Sleep")," "),end="\t")
                else:
                    print(detail,end="\t")
            print()
  
        print("""

        Previous [p]                                             Next [n]
              
        Home     [0]                                      Add To Cart [x]
        
        """)
        # Exit Navigation to Home
        x=input("Enter Input ::: \t")
        if x=='0' or x=='o':
            self.display_home()
        elif x=="n":
            if total <=10:
                self.display_searched_books(title=title,offset=0)
            else:
                offset+=10
                if offset >= self.db.total_search_result(title=title):
                    offset = self.db.total_search_result(title=title)-10
                    self.display_searched_books(title=title,offset=offset)
                else:
                    self.display_searched_books(title=title,offset=offset)
        elif x=="p":
            offset-=10
            if offset<=0:
                offset=0
                self.display_searched_books(title=title,offset=offset)
            else:
                self.display_searched_books(title=title,offset=offset)
        elif x=="x":
            self.add_to_cart()
        else:
            self.display_unauthorized()
    
    #+++++Book Management+++++++++++++++++++++++++++++++++++++

    # [2] Book Management......................[ok]

    # Display
    def display_add_book_menu(self):
        self.clear_screen()
        print(self.display_header()+f"""
            Book Management
                            
              [0] Home
              [1] New Book
              [2] Restocking

            """)

        add_book_response = input("Enter the action...")
        return add_book_response
    
    # Add Books :: Logics [Create & Update]
    def add_book_action(self,add_book_response):
        self.clear_screen()
        # Exit Navigation to Home
        if add_book_response=="0":
            self.display_home()

        # Add New Book Entry to Database
        if add_book_response == "1":
            print(self.display_header()+"New Book to Insert")
            book = self.db.create_book()
            self.db.add_books_to_table(**book) # **dict() -> Dictionary Unpacking...

        # Updating the Qty in Existing Book
        elif add_book_response == "2":
            print(self.display_header()+"Update stock Count")
            book=self.db.create_update_book()
            self.db.update_book_quantity_on_re_stocking(**book)
        # Exit Navigation to Home
        else:
            print(self.display_header()+"Wrong INPUT.... :(")
            time.sleep(2)
            self.display_home()

    # User Management :: Login / Logout / SignUp
    # [Customer].............................................[Completed]
    # if:    Name and Email in Customer >> No Issue
    # else:  Create Customer in Customers Table!    
    def display_login(self):
        print(self.display_header()+f"""              
                    [1]  Login with valid Email
                    [2]  Register Customer
                    [3]  Logout
                    """
                    )
        # Login
        login_input=input()
        if login_input == "1" and self.customerName=="Anonymous":
            email = pyinp.inputEmail("Enter your Email...\t")
            if email in self.db.list_emails():
                customer_details = self.db.get_customer_details(email=email)
                print(customer_details[1],"Logged IN SuccessFully...")
                print("You'll be Redirected Shortly to HOME!!!...")
                self.customerName=customer_details[1]
                self.customerEmail=email
                self.customerid=customer_details[0]
                self.customerDetails=customer_details
                time.sleep(2)
                self.display_home()
            # Sign Up Process  [implicit]
            # Sign Up ends and Redirects to LOGIN
            else:
                print("Register Now with the email")
                print(self.display_header()+" Register Now  & Login !!!")
                customer = self.db.create_customer()
                self.db.add_customer_to_table(**customer)
                self.display_login()
        elif login_input=="1" and self.customerName!="Anonymous":
            self.list_of_purchase=dict()
            email = pyinp.inputEmail("Enter your Email...\t")
            if email in self.db.list_emails():
                customer_details = self.db.get_customer_details(email=email)
                print(customer_details[1],"Logged IN SuccessFully...")
                print("You'll be Redirected Shortly to HOME!!!...")
                self.customerName=customer_details[1]
                self.customerEmail=email
                self.customerid=customer_details[0]
                self.customerDetails=customer_details
                time.sleep(2)
                self.display_home()
            # Sign Up Process  [implicit]
            # Sign Up ends and Redirects to LOGIN
            else:
                print("Register Now with the email")
                print(self.display_header()+" Register Now  & Login !!!")
                customer = self.db.create_customer()
                self.db.add_customer_to_table(**customer)
                self.display_login()

        # Sign Up process [explicit]
        # Sign Up ends and Redirects to LOGIN
        elif login_input=="2":
            # New Customer Creation Progress
            print("Register Now")
            print(self.display_header()+" Register Now  & Login !!!")
            customer = self.db.create_customer()
            self.db.add_customer_to_table(**customer)
            self.display_login()

        # Logout :: Clearing the cart and data...   
        elif login_input == "3":
            self.logout()
        else:
            self.display_unauthorized()
    
    def logout(self):
        self.customerName="Anonymous"
        self.customerEmail="Kindly Login in!!!"
        self.customerid="[+]"
        self.list_of_purchase=dict()
        self.display_home()
    
    #+++++Purchase Management+++++++++++++++++++++++++++++++++++++
    """
    To Make a Purchase 
    [Add to Cart [Phase 1], Checkout [Phase 2]] { PLAN !? }

    User need to Provide [Input]
     
      Customer >>>  Name, Email [Password Less Login...]...............[ok]

      Book     >>>  Title, Author, Qty.................................[ok]
      [Search Books and Add using Book ID] [Add Book ID explaination in Sales page]

    [Output] :: Bill Need to Generate

    Dear Customer {Name}, {city}

    You purchases on {date-time}

    S.no,Title, Author, Price, Qty, total
    1   xxx     xxxx    299.99  x1  299.99
    2.  yyy     yyyy    200.00  x2  400.00
    ______________________________________

    Grand Total                     699.99


    [Customer can't add extra then given qty in table]

    [Update]
    Sales Table | Insert Query
    +++++++++++++++++++++++++++++++++++|
    | customer ID   -> select query 1  |
    | book Id       -> select query 2  |
    | quantity sold -> function input  |
    | datetime      -> time module     |
    +++++++++++++++++++++++++++++++++++|
"""
    def display_purchase_page(self):
        print(self.display_header()+"""
                    Purchase Page ::
                    From Search page you can initiate Add to Cart

                    For Search   [s] 
                                        To find the Book Id
                    For Purchase [x] 
                                        Followed By [*Book Id*] and Quantity [Number]
                    For Checkout [c] 
                                        To Check OUT

                    """)
        purchase_input = input()

        # For Sales Table
        # sales Id, Book Id, Customer Id, Qty, date [Y-M-D]
        if purchase_input == 's':
            print("Kindly Note down the Book ID is More Like Product Id for Purchase")
            title = pyinp.inputStr(prompt="Enter the Title Keyword\t")
            self.display_searched_books(title=title,offset=0)
        elif purchase_input == "x":
            self.add_to_cart()
        elif purchase_input=="c" and self.customerName!="Anonymous":
            self.gen_bill()
            # print(self.list_of_purchase)
            input()
            # time.sleep(1)
            self.display_home()
        else:
            self.display_purchase_page()

    # SOME BUG IS STILL HERE !!!
    def add_to_cart(self):
        # User can't add to cart when he is Anonymous
        if self.customerName == "Anonymous":
            print("Not Allowed to Purchase book\nPlease Login...")
            self.display_login()
        else:
            customerId=self.customerid
            bookId = pyinp.inputInt(prompt="Enter the Book Id\t",max=self.db.total_books_entries(),min=1)
            stock_of_book=self.db.check_stock(bookId)[0]
            if stock_of_book == 0: 
                # Case: If No Stock available | it shows the message & navigate to Catalogue...
                print("No Stock Available right Now!!!")
                print(*self.db.get_book_details(bookid=bookId)[0],sep="\t")
                time.sleep(2)
                self.display_all_books()
            else:
                print(stock_of_book, "Stock Is available")
                quantity = pyinp.inputInt(prompt="Kindly enter the Quantity...\t",min=1,max=stock_of_book)
                # Sales Table Entity
                x=[customerId,quantity,self.datenow]
                if bookId in self.list_of_purchase.keys():
                    new_qty=self.list_of_purchase[bookId][1]+quantity
                    if new_qty > stock_of_book:
                        print(f"Max stocked in {stock_of_book} so {new_qty} books can't be delivered...")
                        print(f"Will Be Re-stocked in Every Monday")
                        time.sleep(1)
                        new_qty=stock_of_book
                    self.list_of_purchase[bookId][1]=new_qty
                    time.sleep(1)
                    self.display_purchase_page()
                else:
                    self.list_of_purchase[bookId]=x
                    # print(self.list_of_purchase)
                    time.sleep(1)
                    self.display_purchase_page()

    # S.no Title, Author, Price, Qty, total
    # 1   xxx     xxxx    299.99  x1  299.99
    # 2   yyy     yyyy    200.00  x2  400.00
    # ______________________________________

    # Grand Total                     699.99
    def gen_bill(self):
        salesEntry=[[x]+self.list_of_purchase[x] for x in self.list_of_purchase]
        print(tabulate(salesEntry))
        # print("In GEN BILL SECTION",salesEntry) # For DEBUG
        bill_det=[]
        for i in salesEntry:
            data=self.db.get_book_details(i[0])[0]
            # print(data) # FOR DEBUGGING
            bill_det.append([i[0],data[1],data[2],data[4],i[2],data[4]*i[2]])
        # print(salesEntry)
        str1=f"""
            Dear Customer {self.customerDetails[1]}, {self.customerDetails[3]}

            You purchases on {datetime.now().strftime("%d, %B %Y [%H:%M]")}

        """
        print(str1)
        x=tabulate(bill_det,headers=["Book Id","Title","Author","Price","Purchased Quants","Total"],tablefmt="grid")
        for i in x.splitlines():
            print(i.center(shutil.get_terminal_size().columns-20," "))
        print(f"""
            Grand Total {sum([x[-1] for x in bill_det])}

            Thank You Visit us Any time.""")
            
        gen_bill_response=input("\t\tTo Confirm the Purchase\n"+
                                "\t\t[Yes] (y)          [No] (n)\n")
        
        if gen_bill_response.lower() == "y" or gen_bill_response.lower()=="yes":            
            # Sales Table Update Entry...
            self.db.update_sales_data(sales_data=salesEntry)
            # Stock Update in Books...
            for data in salesEntry:
                self.db.update_book_quantity_on_purchase(data[0],data[2])
            print(self.display_header()+"\nPurchase is DONE\nThank You Visit us Again")
            self.list_of_purchase.clear()
            print(self.list_of_purchase,"Cleared Paid")
            input()
            self.display_all_books()
        else:
            response=input("[0] To Clear cart\n[1] To Logout")
            if response == "0":
                self.list_of_purchase.clear()
                # print(self.list_of_purchase)
            elif response == "1":
                self.logout()
            else:
                self.display_unauthorized()

    # Purchase Management 

    #+++++Purchase Review+++++++++++++++++++++++++++++++++++++

    def display_all_purchase(self,offset=0,email=None):
        print(self.display_header())
        total_purchase_count=self.db.get_purchase_details(offset,email=email)[1][0]
        print(tabulate([[x]+[*y] for x,y in enumerate(self.db.get_purchase_details(offset,email=email)[0])],tablefmt="grid"))
        print(f"""
        next   [n]                                                      previous [p]
              
        filter [f]                                                         home  [0]

        """)
        response=input()
        self.clear_screen()
        
        if response == "n" and total_purchase_count >=11:
            offset+=10
            if offset > total_purchase_count:
                offset=total_purchase_count-10
            # print(tabulate(self.db.get_purchase_details(offset),tablefmt="grid"))
            self.display_all_purchase(offset,email=email)
        elif response=="p" and total_purchase_count >=11:
            offset-=10
            if offset < 0:
                offset=0
            self.display_all_purchase(offset,email=email)
        elif response=="f": 
            email=pyinp.inputEmail("Enter the Email for filter...")
            if email in self.db.list_emails():
                self.display_all_purchase(offset,email=email)
                print("Email Output")
            else:
                print("Enter email is not Listed in BookStore 101")
                time.sleep(1)
                self.display_all_purchase()
        elif response == "0":
            self.display_home()
        else:
            if response in ("n","p"):
                print(f"Total Purchase is {total_purchase_count} so pagination not required...")
                input()
                self.display_all_purchase(offset,email=email)
            else:
                self.display_all_purchase(offset,email=email)

    #+++++User Details+++++++++++++++++++++++++++++++++++++
    def display_customer_page(self,offset=0):
        x=self.db.get_user_details()
        total_user=x[1]
        print(self.display_header())
        print(tabulate(x[0],tablefmt="grid"))
        print(f"""
        next    [n]                                                      previous [p]
              
        details [d]                                                         home  [0]

        """)
        response=input()
        self.clear_screen()
        
        if response == "n" and total_user >=11:
            offset+=10
            if offset > total_user:
                offset=total_user-10
            # print(tabulate(self.db.get_purchase_details(offset),tablefmt="grid"))
            self.display_customer_page(offset)
        elif response=="p" and total_user >=11:
            offset-=10
            if offset < 0:
                offset=0
            self.display_customer_page(offset)
        elif response=="d": 
            userid=pyinp.inputNum("Enter the Customer Id for Detail...",min=1,max=total_user)
            print(userid," << UserId")
            off=0
            self.user_details(offset=off,id=userid)
        elif response == "0":
            self.display_home()
        else:
            if response in ("n","p"):
                print(f"Total User is {total_user} so pagination not required...")
                input()
                self.display_customer_page(offset)
            else:
                self.display_customer_page(offset)
    
    def user_details(self,offset,id):
        user_data1=self.db.overall_purchase_summary(id)
        print(self.display_header()+f"""

        Name : {user_data1[1]}                 
        Email: {user_data1[2]}


        Total Number of Books Purchase: {user_data1[3]}
        Total Amount Spent  : {user_data1[4]}

        """)
        data=self.db.get_purchase_det_by_user(offset,id)
        total_count=data[1][0]
        print(tabulate(data[0],tablefmt="grid"))
        print(f"""
        next    [n]                                                      previous [p]
              
        home    [0]

        """)
        response=input()
        # self.clear_screen()
        if response == "n" and total_count >=11:
            offset+=10
            if offset > total_count:
                offset=total_count-10
            self.user_details(offset,id)
        elif response=="p" and total_count >=11:
            offset-=10
            if offset < 0:
                offset=0
            self.user_details(offset,id)
        elif response == "0":
            self.display_home()
        else:
            if response in ("n","p"):
                print(f"Total Count is {total_count} so pagination not required...")
                input()
                self.user_details(offset,id)
            else:
                self.display_unauthorized()

    def most_valuble_records(self):
        master_data=self.db.most_valuble_records_data()
        data=master_data[0]
        # print(data,"Check the FOrmat please")
        print(self.display_header()+f"""
              
        ,....,
      ,::::::<              Most Valuable Customer of Bookstore 101 || {datetime.now().strftime("%Y")} ||
     ,::/^\"``.
    ,::/, `   e`.           Name            : {data[1]}
   ,::; |        '.
   ,::|  \___,-.  c)        Email           : {data[2]}
   ;::|     \   '-'
   ;::|      \              Location        : {data[3]}
   ;::|   _.=`
                            Total Books     : {data[4]}

                            Total Amount    : {data[5]}
        
        Home  [0]

        """)
        print("LeaderBoard [1] >>> \n"+tabulate(master_data,tablefmt="grid"))
        res=input()
        if res == "0":
            self.display_home()
        else:
            self.most_valuble_records()