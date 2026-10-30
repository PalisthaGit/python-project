# Book API

A simple REST API built with FastAPI to manage a list of books.
Built as a learning project: I wrote every endpoint myself.

## Features
- Get all books, or one book by id
- Add, update and delete books
- Input validation with Pydantic
- 404 errors when a book is not found

## Setup
1. Install the packages:
   pip install -r requirements.txt
2. Start the server:
   python3 -m uvicorn main:app --reload
3. Open the interactive docs at http://127.0.0.1:8000/docs

## Endpoints
| Method | Path | What it does |
|--------|------|--------------|
| GET | / | Check that the API is running |
| GET | /books | Get all books |
| GET | /books/{book_id} | Get one book |
| POST | /books | Add a new book |
| PUT | /books/{book_id} | Update a book |
| DELETE | /books/{book_id} | Delete a book |

## Example request body (POST and PUT)
{
  "title": "Book title",
  "author": "Author name"
}

## Notes
- Data is stored in a Python list, so it resets when the server restarts.
- New ids use the biggest existing id + 1, so ids never repeat after a delete.