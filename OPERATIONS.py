from db import get_db_connection

def add_book(title, author):
    db = get_db_connection()
    cursor = db.cursor()
    query = "INSERT INTO books (title, author) VALUES (%s, %s)"
    cursor.execute(query, (title, author))
    db.commit()
    print(f"✅ Book '{title}' by {author} added successfully!")
    db.close()
