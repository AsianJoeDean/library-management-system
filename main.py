from src.catalog import LibraryCatalog

def print_menu():
    print("\n===================================================")
    print("        OAKLAND UNIVERSITY LIBRARY SYSTEM")
    print("===================================================")
    print(" 1. Add a New Book")
    print(" 2. Search by ISBN")
    print(" 3. Search by Title")
    print(" 4. Search by Author")
    print(" 5. View All Books (A-Z)")
    print(" 6. Borrow a Book")
    print(" 7. Return a Book")
    print(" 8. Remove from Waitlist")
    print(" 9. Exit")
    print("===================================================")

def main():
    # Initialize the core backend
    my_library = LibraryCatalog()

    # Pre-load data for the demo
    my_library.add_new_book("The Great Gatsby", "F. Scott Fitzgerald", "111")
    my_library.add_new_book("1984", "George Orwell", "222")
    my_library.add_new_book("Animal Farm", "George Orwell", "333")
    my_library.add_new_book("Clean Code", "Robert C. Martin", "444")

    # The main application loop
    while True:
        print_menu()
        choice = input("Select an option (1-9): ")

        if choice == '1':
            title = input("Enter Book Title: ")
            author = input("Enter Author: ")
            isbn = input("Enter ISBN: ")
            print("\n--- Processing ---")
            my_library.add_new_book(title, author, isbn)

        elif choice == '2':
            isbn = input("Enter ISBN to search: ")
            print("\n--- Processing ---")
            book = my_library.find_book(isbn)
            if book:
                print(f"RESULT: {book}")
            else:
                print("Book not found.")

        elif choice == '3':
            title = input("Enter Book Title to search: ")
            print("\n--- Processing ---")
            books = my_library.search_by_title(title)
            if books:
                print(f"Found {len(books)} match(es):")
                for b in books:
                    print(f" - {b}")
            else:
                print("No books found with that title.")

        elif choice == '4':
            author = input("Enter Author to search: ")
            print("\n--- Processing ---")
            books = my_library.search_by_author(author)
            if books:
                print(f"Found {len(books)} book(s) by {author}:")
                for b in books:
                    print(f" - {b}")
            else:
                print("No books found by that author.")

        elif choice == '5':
            my_library.display_all_sorted()

        elif choice == '6':
            isbn = input("Enter ISBN to borrow: ")
            user = input("Enter your name: ")
            print("\n--- Processing ---")
            my_library.borrow_book(isbn, user)

        elif choice == '7':
            isbn = input("Enter ISBN to return: ")
            print("\n--- Processing ---")
            my_library.return_book(isbn)

        elif choice == '8':
            isbn = input("Enter ISBN for the waitlist: ")
            user = input("Enter your name: ")
            print("\n--- Processing ---")
            my_library.cancel_waitlist(isbn, user)

        elif choice == '9':
            print("\nExiting Library System. Goodbye!")
            break
            
        else:
            print("\nInvalid option. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()