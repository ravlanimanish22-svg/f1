from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_books_crud():
    # First create an admin
    client.post(
        "/v1/auth/register",
        json={
            "username": "admin",
            "email": "admin@example.com",
            "password": "adminpass",
            "role": "admin",
            "is_admin": True
        }
    )

    # Login as admin
    response = client.post(
        "/v1/auth/token",
        data={"username": "admin", "password": "adminpass"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create book
    response = client.post(
        "/v1/books",
        json={
            "title": "Test Book",
            "author": "Author",
            "isbn": "1234567890",
            "publication_year": 2024,
            "genre": "Fiction",
            "description": "A test book"
        },
        headers=headers
    )
    assert response.status_code == 200
    book = response.json()
    book_id = book["id"]

    # Get book
    response = client.get(f"/v1/books/{book_id}")
    assert response.status_code == 200

    # Update book
    response = client.put(
        f"/v1/books/{book_id}",
        json={"title": "Updated Book"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Updated Book"

    # Delete book
    response = client.delete(f"/v1/books/{book_id}", headers=headers)
    assert response.status_code == 200
