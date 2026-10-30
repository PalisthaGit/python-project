from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

books = [
    {
        "id":1,
        "title":"Book 1",
        "author": "Author 1",
    },

    {
        "id":2,
        "title":"Book 2",
        "author": "Author 2"
    }

]

app = FastAPI()

class BookIn(BaseModel):
    title: str
    author: str

@app.get("/")
def home():
    return {"message": "Book API is running"}


@app.get("/books")
def get_books():
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book_id == book["id"]:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books")
def add_book(book: BookIn):
    biggest_id = 0
    for existing_book in books:
        if existing_book['id']> biggest_id:
            biggest_id = existing_book['id']
    new_book = {
        "id": biggest_id+1,
        "title":book.title,
        "author":book.author
    }
    books.append(new_book)
    return new_book

@app.delete("/books/{book_id}")
def delete_book(book_id:int):
    for book in books:
        if book_id == book["id"]:
            books.remove(book)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{book_id}")
def update_book(book_id:int, book: BookIn):
    for existing_book in books:
        if existing_book['id'] == book_id:
            existing_book['title'] = book.title
            existing_book['author'] = book.author
            return existing_book
    raise HTTPException(status_code=404, detail = "Book not found")
        

