# Library Management System

This is a GUI-based Library Management System built for our final semester at Oakland University. The program handles standard book inventory operations and includes a dynamic waitlist feature. It is collaboratively built using Python, Tkinter, and optimized data structures to ensure fast search and queue operations.

## Features
* Add, search, and return books using a custom Tkinter graphical interface.
* Optimized O(1) search complexity using Python dictionaries (Hash Tables) for ISBN, Title, and Author lookups.
* Automated waitlist management using `collections.deque` to enforce strict First-In-First-Out (FIFO) checkout rules.
* Live status dashboard that automatically sorts the catalog alphabetically.

## Setup and Installation
This project uses standard Python libraries, so no external package installations are required.
* **Prerequisites:** Python 3.x must be installed on your machine.

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/AsianJoeDean/library-management-system.git
   ```
2. Navigate into the project folder:
   ```bash
   cd library-management-system
   ```
3. Run the main file to launch the GUI:
   ```bash
   python main.py
   ```

## Usage Instructions
* **Adding a Book:** Enter the Title, Author, and ISBN in the top-left fields and click "Add New Book". The Live Status table will update automatically.
* **Searching:** Select either the "ISBN" or "Book Title" radio button, type your query, and click "Search Book". You can also search by author using the dedicated button.
* **Borrowing:** Enter the book's ISBN and a User Name. Click "Borrow Book". If the book is already checked out, the system will automatically place the user on the waitlist.
* **Returning:** Enter the ISBN and click "Return Book". If there is an active waitlist for that book, it will instantly be checked out to the next person in the queue.

## Project Structure
* `main.py`: Contains the Tkinter GUI and frontend logic.
* `src/catalog.py`: Contains the backend logic, Hash Table indexes, and core library functions.
* `src/book.py`: Contains the Book data model and individual waitlist queues.
