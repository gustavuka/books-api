from datetime import date

import pytest
from fastapi.testclient import TestClient

from app.models.book import Book

# Test data
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
}

TEST_BOOK = {
    "title": "Test Book",
    "author": "Test Author",
    "published_date": date(2023, 1, 1).isoformat(),
    "summary": "A test book description",
    "genre": "Test Genre",
}


@pytest.fixture
def test_user_token(client: TestClient, test_user):
    """Get authentication token for test user"""
    response = client.post(
        "/auth/login",
        json={"username": TEST_USER["username"], "password": TEST_USER["password"]},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def created_book(db_session):
    """Create a test book directly in the database and return it"""
    # Convert ISO string back to date for database model
    book_data = TEST_BOOK.copy()
    book_data["published_date"] = date.fromisoformat(book_data["published_date"])
    book = Book(**book_data)
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    return book


def test_create_book_unauthenticated(client: TestClient):
    """Test that creating a book without authentication fails"""
    response = client.post("/books/", json=TEST_BOOK)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_book_authenticated(client: TestClient, test_user_token):
    """Test that creating a book with authentication succeeds"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    response = client.post("/books/", json=TEST_BOOK, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == TEST_BOOK["title"]
    assert data["author"] == TEST_BOOK["author"]
    assert data["published_date"] == TEST_BOOK["published_date"]
    assert data["summary"] == TEST_BOOK["summary"]
    assert data["genre"] == TEST_BOOK["genre"]
    assert "id" in data


def test_get_book_authenticated(client: TestClient, test_user_token, created_book):
    """Test that getting a book with authentication succeeds"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    response = client.get(f"/books/{created_book.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_book.id
    assert data["title"] == TEST_BOOK["title"]
    assert data["author"] == TEST_BOOK["author"]
    assert data["published_date"] == TEST_BOOK["published_date"]
    assert data["summary"] == TEST_BOOK["summary"]
    assert data["genre"] == TEST_BOOK["genre"]


def test_get_nonexistent_book(client: TestClient, test_user_token):
    """Test that getting a nonexistent book returns 404"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    response = client.get("/books/999999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Book with id 999999 not found"


def test_create_book_invalid_data(client: TestClient, test_user_token):
    """Test that creating a book with invalid data fails"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    invalid_book = {
        "title": "",
        "author": "Test Author",
        "published_date": date(2023, 1, 1).isoformat(),
        "summary": "A test book description",
        "genre": "Test Genre",
    }
    response = client.post("/books/", json=invalid_book, headers=headers)
    assert response.status_code == 422


def test_create_book_missing_fields(client: TestClient, test_user_token):
    """Test that creating a book with missing required fields fails"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    incomplete_book = {
        "title": "Test Book",
        "author": "Test Author",
        # Missing published_date
    }
    response = client.post("/books/", json=incomplete_book, headers=headers)
    assert response.status_code == 422  # Validation error


def test_create_book_invalid_date(client: TestClient, test_user_token):
    """Test that creating a book with invalid date fails"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    invalid_date_book = {
        "title": "Test Book",
        "author": "Test Author",
        "published_date": "invalid-date",  # Invalid date format
        "summary": "A test book description",
        "genre": "Test Genre",
    }
    response = client.post("/books/", json=invalid_date_book, headers=headers)
    assert response.status_code == 422  # Validation error
