from Display._01display_store import DisplayStore
class Runner:
    def run(self):
        display=DisplayStore()
        display.display_home()
        while True:        
            response = input("Enter the Option...")
            if response=="q":
                break

            if response=="1":
                display.display_all_books()

            elif response=="0":
                display.display_home()

            elif response=="2":
                add_book_response=display.display_add_book_menu()
                display.add_book_action(add_book_response)

            elif response=="3":
                display.display_purchase_page()

            elif response=="*":
                display.display_login()

            else:
                display.display_unauthorized()