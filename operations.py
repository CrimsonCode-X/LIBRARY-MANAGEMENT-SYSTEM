from db import get_db_connection
from datetime import date

def add_book(title, author):
    db = get_db_connection()
    cursor = db.cursor()
    query = "INSERT INTO books (title, author) VALUES (%s, %s)"
    cursor.execute(query, (title, author))
    db.commit()
    print(f"Book '{title}' by {author} added successfully!")
    db.close()

def view_books():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    print("\nAll Books:")
    for row in rows:
        status = "Available" if row[3] else "Issued"
        print(f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]} | {status}")
    db.close()

def add_member(name, email):
    db = get_db_connection()
    cursor = db.cursor()
    query = "INSERT INTO members (name, email) VALUES (%s, %s)"
    try:
        cursor.execute(query, (name, email))
        db.commit()
        print(f"Member '{name}' registered successfully!")
    except Exception as e:
        print(f"Error: {e}")
    db.close()

def view_members():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM members")
    rows = cursor.fetchall()
    print("\nAll Members:")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]}")
    db.close()

def issue_book(book_id, member_id):
    db = get_db_connection()
    cursor = db.cursor()

    # Check if book is available
    cursor.execute("SELECT available FROM books WHERE book_id = %s", (book_id,))
    result = cursor.fetchone()
    if not result:
        print("Book not found!")
        db.close()
        return
    if not result[0]:
        print("Book is already issued!")
        db.close()
        return

    query = "INSERT INTO transactions (book_id, member_id, issue_date) VALUES (%s, %s, %s)"
    cursor.execute(query, (book_id, member_id, date.today()))
    cursor.execute("UPDATE books SET available = FALSE WHERE book_id = %s", (book_id,))
    db.commit()
    print(f"Book ID {book_id} issued to Member ID {member_id}")
    db.close()

def return_book(transaction_id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT book_id, return_date FROM transactions WHERE transaction_id = %s", (transaction_id,))
    result = cursor.fetchone()
    if not result:
        print("Transaction not found!")
        db.close()
        return
    if result[1] is not None:
        print("Book already returned!")
        db.close()
        return

    book_id = result[0]
    cursor.execute("UPDATE transactions SET return_date = %s WHERE transaction_id = %s", (date.today(), transaction_id))
    cursor.execute("UPDATE books SET available = TRUE WHERE book_id = %s", (book_id,))
    db.commit()
    print(f"Book ID {book_id} returned successfully!")
    db.close()
