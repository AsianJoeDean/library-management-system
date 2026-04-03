import tkinter as tk
from tkinter import ttk, messagebox
import io
from contextlib import redirect_stdout

from src.catalog import LibraryCatalog


class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Oakland University Library System")
        self.root.geometry("1250x780")
        self.root.configure(bg="#f4f6f8")

        self.my_library = LibraryCatalog()
        self.load_demo_data()
        self.setup_styles()
        self.build_gui()
        self.refresh_status_table()

    def load_demo_data(self):
        demo_books = [
            ("The Great Gatsby", "F. Scott Fitzgerald", "111"),
            ("1984", "George Orwell", "222"),
            ("Animal Farm", "George Orwell", "333"),
            ("Clean Code", "Robert C. Martin", "444"),
        ]

        for title, author, isbn in demo_books:
            if self.my_library.find_book(isbn) is None:
                self.my_library.add_new_book(title, author, isbn)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Title.TLabel",
            font=("Arial", 24, "bold"),
            background="#f4f6f8",
            foreground="#1f2d3d"
        )
        style.configure(
            "Section.TLabel",
            font=("Arial", 12, "bold"),
            background="#ffffff",
            foreground="#1f2d3d"
        )
        style.configure(
            "Custom.TLabelframe",
            background="#ffffff"
        )
        style.configure(
            "Custom.TLabelframe.Label",
            font=("Arial", 12, "bold"),
            background="#ffffff",
            foreground="#1f2d3d"
        )
        style.configure(
            "Custom.TButton",
            font=("Arial", 10, "bold"),
            padding=8
        )
        style.configure(
            "Treeview",
            rowheight=28,
            font=("Arial", 10)
        )
        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

    def build_gui(self):
        title = ttk.Label(
            self.root,
            text="OAKLAND UNIVERSITY LIBRARY SYSTEM",
            style="Title.TLabel"
        )
        title.pack(pady=18)

        main_frame = tk.Frame(self.root, bg="#f4f6f8")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        left_frame = tk.Frame(main_frame, bg="#f4f6f8")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_frame = tk.Frame(main_frame, bg="#f4f6f8")
        right_frame.pack(side="right", fill="both", expand=True)

        self.build_input_section(left_frame)
        self.build_action_buttons(left_frame)
        self.build_output_section(left_frame)
        self.build_status_section(right_frame)

    def build_input_section(self, parent):
        frame = ttk.LabelFrame(parent, text="Book Information", style="Custom.TLabelframe", padding=15)
        frame.pack(fill="x", pady=(0, 12))

        ttk.Label(frame, text="Book Title:", style="Section.TLabel").grid(row=0, column=0, padx=8, pady=8, sticky="e")
        self.title_entry = ttk.Entry(frame, width=35)
        self.title_entry.grid(row=0, column=1, padx=8, pady=8, sticky="w")

        ttk.Label(frame, text="Author:", style="Section.TLabel").grid(row=1, column=0, padx=8, pady=8, sticky="e")
        self.author_entry = ttk.Entry(frame, width=35)
        self.author_entry.grid(row=1, column=1, padx=8, pady=8, sticky="w")

        ttk.Label(frame, text="ISBN:", style="Section.TLabel").grid(row=2, column=0, padx=8, pady=8, sticky="e")
        self.isbn_entry = ttk.Entry(frame, width=35)
        self.isbn_entry.grid(row=2, column=1, padx=8, pady=8, sticky="w")

        ttk.Label(frame, text="User Name:", style="Section.TLabel").grid(row=3, column=0, padx=8, pady=8, sticky="e")
        self.user_entry = ttk.Entry(frame, width=35)
        self.user_entry.grid(row=3, column=1, padx=8, pady=8, sticky="w")

        ttk.Label(frame, text="Use Title / ISBN:", style="Section.TLabel").grid(row=4, column=0, padx=8, pady=8, sticky="e")
        self.lookup_mode = tk.StringVar(value="isbn")

        radio_frame = tk.Frame(frame, bg="#ffffff")
        radio_frame.grid(row=4, column=1, padx=8, pady=8, sticky="w")

        ttk.Radiobutton(radio_frame, text="ISBN", variable=self.lookup_mode, value="isbn").pack(side="left", padx=(0, 12))
        ttk.Radiobutton(radio_frame, text="Book Title", variable=self.lookup_mode, value="title").pack(side="left")

    def build_action_buttons(self, parent):
        frame = ttk.LabelFrame(parent, text="Actions", style="Custom.TLabelframe", padding=15)
        frame.pack(fill="x", pady=(0, 12))

        buttons = [
            ("Add New Book", self.add_book),
            ("Search Book", self.search_book),
            ("Search by Author", self.search_author),
            ("View All Books", self.view_all_books),
            ("Borrow Book", self.borrow_book),
            ("Return Book", self.return_book),
            ("View Waitlist", self.view_waitlist),
            ("Remove from Waitlist", self.remove_waitlist),
            ("Refresh Status", self.refresh_status_table),
            ("Clear Fields", self.clear_fields),
            ("Clear Output", self.clear_output),
        ]

        row = 0
        col = 0
        for text, command in buttons:
            btn = ttk.Button(frame, text=text, command=command, style="Custom.TButton")
            btn.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
            col += 1
            if col > 2:
                col = 0
                row += 1

        for i in range(3):
            frame.columnconfigure(i, weight=1)

    def build_output_section(self, parent):
        frame = ttk.LabelFrame(parent, text="System Output", style="Custom.TLabelframe", padding=12)
        frame.pack(fill="both", expand=True)

        self.output_text = tk.Text(
            frame,
            height=15,
            wrap="word",
            font=("Consolas", 10),
            bg="#fcfcfc",
            fg="#222222",
            relief="solid",
            borderwidth=1
        )
        self.output_text.pack(fill="both", expand=True)

    def build_status_section(self, parent):
        frame = ttk.LabelFrame(parent, text="Live Library Status", style="Custom.TLabelframe", padding=12)
        frame.pack(fill="both", expand=True)

        columns = ("title", "author", "isbn", "status", "waitlist")
        self.status_table = ttk.Treeview(frame, columns=columns, show="headings", height=22)

        self.status_table.heading("title", text="Title")
        self.status_table.heading("author", text="Author")
        self.status_table.heading("isbn", text="ISBN")
        self.status_table.heading("status", text="Status")
        self.status_table.heading("waitlist", text="Waitlist")

        self.status_table.column("title", width=220)
        self.status_table.column("author", width=170)
        self.status_table.column("isbn", width=90, anchor="center")
        self.status_table.column("status", width=110, anchor="center")
        self.status_table.column("waitlist", width=220)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.status_table.yview)
        self.status_table.configure(yscrollcommand=scrollbar.set)

        self.status_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.status_table.bind("<<TreeviewSelect>>", self.on_table_select)

    def on_table_select(self, event):
        selected = self.status_table.selection()
        if not selected:
            return

        values = self.status_table.item(selected[0], "values")
        if len(values) < 4:
            return

        title = values[0]
        author = values[1]
        isbn = values[2]

        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, title)

        self.author_entry.delete(0, tk.END)
        self.author_entry.insert(0, author)

        self.isbn_entry.delete(0, tk.END)
        self.isbn_entry.insert(0, isbn)

    def show_output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)

    def clear_output(self):
        self.output_text.delete("1.0", tk.END)

    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)
        self.user_entry.delete(0, tk.END)

    def capture_print_output(self, func, *args):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            func(*args)
        return buffer.getvalue().strip()

    def get_all_books_from_library(self):
        if hasattr(self.my_library, "books") and isinstance(self.my_library.books, dict):
            return list(self.my_library.books.values())
        return []

    def parse_book_info(self, book):
        return book.title, book.author, book.isbn

    def get_book_status(self, book):
        return "Checked Out" if book.is_checked_out else "Available"

    def get_waitlist_text(self, book):
        if len(book.waitlist) == 0:
            return "No waitlist"
        return ", ".join(list(book.waitlist))

    def find_book_by_title_exact(self, title):
        matches = self.my_library.search_by_title(title)
        if matches:
            return matches[0]
        return None

    def get_book_by_mode(self):
        mode = self.lookup_mode.get()

        if mode == "isbn":
            isbn = self.isbn_entry.get().strip()
            if not isbn:
                messagebox.showerror("Missing Information", "Please enter an ISBN.")
                return None
            book = self.my_library.find_book(isbn)
            if not book:
                self.show_output("Book not found.")
                return None
            return book

        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Missing Information", "Please enter a book title.")
            return None

        book = self.find_book_by_title_exact(title)
        if not book:
            self.show_output("No book found with that exact title.")
            return None
        return book

    def refresh_status_table(self):
        for row in self.status_table.get_children():
            self.status_table.delete(row)

        books = self.get_all_books_from_library()
        books = sorted(books, key=lambda book: book.title.lower())

        for book in books:
            title, author, isbn = self.parse_book_info(book)
            status = self.get_book_status(book)
            waitlist_text = self.get_waitlist_text(book)
            self.status_table.insert("", tk.END, values=(title, author, isbn, status, waitlist_text))

        self.show_output("Status table refreshed.")

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        isbn = self.isbn_entry.get().strip()

        if not title or not author or not isbn:
            messagebox.showerror("Missing Information", "Please enter Title, Author, and ISBN.")
            return

        output = self.capture_print_output(self.my_library.add_new_book, title, author, isbn)
        self.show_output(output if output else f'Added: "{title}" by {author} (ISBN: {isbn})')
        self.refresh_status_table()

    def search_book(self):
        mode = self.lookup_mode.get()

        if mode == "isbn":
            isbn = self.isbn_entry.get().strip()
            if not isbn:
                messagebox.showerror("Missing Information", "Please enter an ISBN.")
                return

            book = self.my_library.find_book(isbn)
            if book:
                self.show_output(f"Search Result (ISBN): {book}")
            else:
                self.show_output("Book not found.")
        else:
            title = self.title_entry.get().strip()
            if not title:
                messagebox.showerror("Missing Information", "Please enter a book title.")
                return

            books = self.my_library.search_by_title(title)
            if books:
                self.show_output(f'Found {len(books)} match(es) for "{title}":')
                for b in books:
                    self.show_output(f" - {b}")
            else:
                self.show_output("No books found with that title.")

    def search_author(self):
        author = self.author_entry.get().strip()
        if not author:
            messagebox.showerror("Missing Information", "Please enter an author name.")
            return

        books = self.my_library.search_by_author(author)
        if books:
            self.show_output(f'Found {len(books)} book(s) by {author}:')
            for b in books:
                self.show_output(f" - {b}")
        else:
            self.show_output("No books found by that author.")

    def view_all_books(self):
        output = self.capture_print_output(self.my_library.display_all_sorted)
        self.show_output(output if output else "No books available.")
        self.refresh_status_table()

    def borrow_book(self):
        user = self.user_entry.get().strip()
        if not user:
            messagebox.showerror("Missing Information", "Please enter a user name.")
            return

        book = self.get_book_by_mode()
        if not book:
            return

        output = self.capture_print_output(self.my_library.borrow_book, book.isbn, user)
        self.show_output(output if output else f"{user} borrowed '{book.title}'.")
        self.refresh_status_table()

    def return_book(self):
        book = self.get_book_by_mode()
        if not book:
            return

        output = self.capture_print_output(self.my_library.return_book, book.isbn)
        self.show_output(output if output else f"Returned '{book.title}'.")
        self.refresh_status_table()

    def view_waitlist(self):
        book = self.get_book_by_mode()
        if not book:
            return

        if len(book.waitlist) == 0:
            self.show_output(f"Waitlist for '{book.title}': No one is currently waiting.")
        else:
            self.show_output(f"Waitlist for '{book.title}':")
            for i, name in enumerate(book.waitlist, start=1):
                self.show_output(f" {i}. {name}")

        self.refresh_status_table()

    def remove_waitlist(self):
        user = self.user_entry.get().strip()
        if not user:
            messagebox.showerror("Missing Information", "Please enter a user name.")
            return

        book = self.get_book_by_mode()
        if not book:
            return

        output = self.capture_print_output(self.my_library.cancel_waitlist, book.isbn, user)
        self.show_output(output if output else f"{user} removed from waitlist for '{book.title}'.")
        self.refresh_status_table()


def main():
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()