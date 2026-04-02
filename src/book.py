from collections import deque

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_checked_out = False
        # Each book has its own waitlist queue
        self.waitlist = deque() 

    def __str__(self):
        status = "Checked Out" if self.is_checked_out else "Available"
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - [{status}]"