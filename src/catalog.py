from src.book import Book

class LibraryCatalog:
    def __init__(self):
        # Primary Hash Table
        self.books = {}
        # Secondary Hash Tables for O(1) lookups
        self.title_index = {}
        self.author_index = {}

    def _add_to_indexes(self, book):
        """Helper method to add a book to the secondary indexes."""
        title_key = book.title.lower()
        author_key = book.author.lower()
        
        # Add to title index
        if title_key not in self.title_index:
            self.title_index[title_key] = []
        self.title_index[title_key].append(book)
        
        # Add to author index
        if author_key not in self.author_index:
            self.author_index[author_key] = []
        self.author_index[author_key].append(book)

    def _remove_from_indexes(self, book):
        """Helper method to clean up secondary indexes when a book is removed/updated."""
        title_key = book.title.lower()
        author_key = book.author.lower()
        
        if title_key in self.title_index and book in self.title_index[title_key]:
            self.title_index[title_key].remove(book)
        if author_key in self.author_index and book in self.author_index[author_key]:
            self.author_index[author_key].remove(book)

    def add_new_book(self, title, author, isbn):
        if isbn in self.books:
            print(f"Error: ISBN {isbn} already exists in catalog.")
            return
        
        new_book = Book(title, author, isbn)
        self.books[isbn] = new_book
        self._add_to_indexes(new_book)
        print(f"Added: {title}")

    def find_book(self, isbn):
        return self.books.get(isbn, None)

    def search_by_title(self, title):
        """O(1) search for all books matching a title."""
        results = self.title_index.get(title.lower(), [])
        return results

    def search_by_author(self, author):
        """O(1) search for all books by a specific author."""
        results = self.author_index.get(author.lower(), [])
        return results

    def borrow_book(self, isbn, user_name):
        book = self.find_book(isbn)
        if not book:
            print(f"Error: No book found with ISBN {isbn}.")
            return

        if not book.is_checked_out:
            book.is_checked_out = True
            print(f"Success: '{book.title}' has been checked out to {user_name}.")
        else:
            book.waitlist.append(user_name) 
            position = len(book.waitlist)
            print(f"Waitlist: '{book.title}' is currently checked out. {user_name} added to waitlist (Position {position}).")

    def return_book(self, isbn):
        book = self.find_book(isbn)
        if not book:
            print(f"Error: No book found with ISBN {isbn}.")
            return

        if not book.is_checked_out:
            print(f"Notice: '{book.title}' is already available.")
            return

        if len(book.waitlist) > 0:
            next_user = book.waitlist.popleft()
            print(f"Returned: '{book.title}' was returned and instantly checked out to {next_user} from the waitlist.")
        else:
            book.is_checked_out = False
            print(f"Returned: '{book.title}' is now available on the shelf.")

    def remove_book(self, isbn):
        if isbn in self.books:
            book = self.books[isbn]
            if len(book.waitlist) > 0:
                print(f"Warning: '{book.title}' has a waitlist. Deleting anyway.")
            
            # Remove from all 3 Hash Tables
            self._remove_from_indexes(book)
            del self.books[isbn]
            print(f"Deleted: Book with ISBN {isbn} has been removed from the catalog.")
        else:
            print(f"Error: Cannot delete. No book found with ISBN {isbn}.")

    def update_book(self, isbn, new_title=None, new_author=None):
        book = self.find_book(isbn)
        if not book:
            print(f"Error: Cannot update. No book found with ISBN {isbn}.")
            return

        # Remove old index records, update the data, then rebuild index records
        self._remove_from_indexes(book)
        
        if new_title:
            book.title = new_title
        if new_author:
            book.author = new_author
            
        self._add_to_indexes(book)
        print(f"Updated: Book {isbn} is now '{book.title}' by {book.author}.")

    def cancel_waitlist(self, isbn, user_name):
        book = self.find_book(isbn)
        if not book:
            return

        try:
            book.waitlist.remove(user_name)
            print(f"Success: {user_name} has been removed from the waitlist for '{book.title}'.")
        except ValueError:
            print(f"Error: {user_name} is not on the waitlist for '{book.title}'.")

    def display_all_sorted(self):
        """Sorts and displays all books alphabetically by title."""
        if not self.books:
            print("The library is currently empty.")
            return

        # Grab all the book objects and sort them by their title attribute
        sorted_books = sorted(self.books.values(), key=lambda book: book.title.lower())
        
        print("\n--- Complete Library Catalog (A-Z) ---")
        for book in sorted_books:
            print(f" - {book}")
        print("--------------------------------------")