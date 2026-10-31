from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_book_not_found():

    response = client.get("/books/333")
    assert response.status_code == 404

def test_add_book():
    response = client.post("/books", json= {"title":"1d", "author":"adf"})
    assert response.status_code ==200
    data = response.json()
    assert data["title"] == "1d"

def test_book_found():
    response = client.get("/books/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Book 1"

def test_home_books():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Book API is running"

def test_update_book():
    response = client.put("/books/1", json= {"title": "Roka", "author": "dfdf"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Roka"

def test_update_book_not_found():
    response = client.put("/books/34343", json= {"title":"343", "author":"fsadf"})
    assert response.status_code == 404

def test_delete_book():
    response = client.delete("/books/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Book deleted"

def test_delete_book_not_found():
    response = client.delete("/books/234234")
    assert response.status_code == 404
