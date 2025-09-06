from OPERATIONS import add_book, add_member, issue_book, return_book, view_books, view_members

def menu():
    while True:
        print("\n===== Library Management System =====")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Register Member")
        print("4. View All Members")
        print("5. Issue Book")
        print("6. Return Book")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            add_book(title, author)

        elif choice == "2":
            view_books()

        elif choice == "3":
            name = input("Enter member name: ")
            email = input("Enter member email: ")
            add_member(name, email)

        elif choice == "4":
            view_members()

        elif choice == "5":
            book_id = int(input("Enter book ID to issue: "))
            member_id = int(input("Enter member ID: "))
            issue_book(book_id, member_id)

        elif choice == "6":
            transaction_id = int(input("Enter transaction ID to return: "))
            return_book(transaction_id)

        elif choice == "7":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    menu()
