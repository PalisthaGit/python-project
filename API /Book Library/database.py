import sqlite3

def create_table():


    connection = sqlite3.connect("books.db")

    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS books(

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL,
    year INTEGER )
    """)

    connection.commit()
    connection.close()

    print("Table created")

def get_all_books():


    connection = sqlite3.connect("books.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM books")

    rows = cursor.fetchall()

    connection.close()

    return rows

def get_book_by_id(book_id):
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id, ))
    row = cursor.fetchone()
    connection.close()
    return row

def update_book(book_id, title, author, genre, year):
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE books SET title = ?, author = ?, genre=?, year = ? WHERE id = ?", (title, author, genre, year, book_id))
    updated = cursor.rowcount
    connection.commit()
    connection.close()
    return updated >0

def delete_book(book_id):
    connection = sqlite3.connect("books.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id, ))
    deleted = cursor.rowcount
    connection.commit()
    connection.close()
    return deleted > 0

def add_book(title, author, genre, year):

    connection = sqlite3.connect("books.db")

    cursor = connection.cursor()

    cursor.execute("INSERT INTO books(title, author, genre, year) VALUES(?, ?, ?, ?)", (title, author, genre, year))

    connection.commit()
    connection.close()
    print("Book Added")
