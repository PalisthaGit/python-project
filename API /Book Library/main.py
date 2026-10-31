from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database


def row_to_dict(row):
    return {
        "id":row[0],
        "title":row[1],
        "author":row[2],
        "genre":row[3],
        "year": row[4]

    }


app = FastAPI()
database.create_table()


class BookIn(BaseModel):
    title: str
    author: str
    genre: str
    year: int

@app.get("/")
def home():
    return {"message": "Book API is running"}


@app.get("/books")
def get_books():
    rows = database.get_all_books()
    result = []
    for row in rows:
        result.append(row_to_dict(row))
    return result

@app.get("/books/{book_id}")
def get_book(book_id: int):
    row= database.get_book_by_id(book_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return row_to_dict(row)

@app.post("/books")
def add_book(book: BookIn):
    database.add_book(book.title, book.author, book.genre, book.year)
    return {"message": "Book was added"}

@app.delete("/books/{book_id}")
def delete_book(book_id:int):
    if database.delete_book(book_id):
        return {"message": "Book deletled"}
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{book_id}")
def update_book(book_id:int, book: BookIn):
    if database.update_book(book_id, book.title, book.author, book.genre, book.year):
        return {"message": "Book updated"}
    raise HTTPException(status_code=404, detail = "Book not found")
        

