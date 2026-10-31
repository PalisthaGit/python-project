# Book API

A simple REST API to manage a library of books. It is built with Python, FastAPI and SQLite. Books are saved in a database file, so they stay after the server stops.

## Features

- Add a book
- See all books
- See one book by its id
- Update a book
- Delete a book
- Clear 404 message when a book is not found

## Tech used

- Python 3
- FastAPI
- SQLite (using Python's `sqlite3`)

## Project files

- `main.py`: the FastAPI app and its endpoints
- `database.py`: all the SQLite functions (create table, add, get, update, delete)
- `requirements.txt`: the packages the project needs

## How to run it

1. Download the project and open the folder in the terminal.

2. Make a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the packages:

```bash
pip install -r requirements.txt
```

4. Start the server:

```bash
fastapi dev main.py
```

5. Open `http://127.0.0.1:8000/docs` in your browser to try the API.

The database file (`books.db`) and its table are created automatically when the app starts.

## Endpoints

| Method | Path | What it does |
|--------|------|--------------|
| GET | `/` | Shows that the API is running |
| GET | `/books` | Gives all books |
| GET | `/books/{book_id}` | Gives one book |
| POST | `/books` | Adds a new book |
| PUT | `/books/{book_id}` | Updates a book |
| DELETE | `/books/{book_id}` | Deletes a book |

## Example book

```json
{
  "title": "Atomic Habits",
  "author": "James Clear",
  "genre": "Self Help",
  "year": 2018
}
```