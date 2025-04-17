# Books API

A FastAPI application for managing a collection of books with real-time updates.

## Features

-   CRUD operations for books
-   JWT-based authentication
-   Real-time updates using Server-Sent Events (SSE)

## API Endpoints

### Users

-   `POST /users/`
    -   Register a new user
    -   Required fields: username, email, password
    -   Example:
        ```json
        {
            "username": "johndoe",
            "email": "john@example.com",
            "password": "securepassword123"
        }
        ```

### Authentication

-   `POST /auth/login`
    -   Authenticate and get JWT token
    -   Required fields: username, password

### Books

-   `GET /books/`

    -   List all books with pagination
    -   Query parameters:
        -   `skip`: Number of records to skip (default: 0)
        -   `limit`: Number of records to return (default: 20, max: 100)

-   `GET /books/{book_id}`

    -   Get a specific book by ID

-   `POST /books/`

    -   Create a new book
    -   Required fields: title, author, published_date, summary, genre

-   `PATCH /books/{book_id}`

    -   Update a book's details
    -   Accepts partial updates

-   `DELETE /books/{book_id}`

    -   Delete a book

-   `GET /books/stream`
    -   Real-time updates stream
    -   Returns Server-Sent Events for new books

## Book Schema

```json
{
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "published_date": "1925-04-10",
    "summary": "A story of the fabulously wealthy Jay Gatsby...",
    "genre": "Classic Literature"
}
```

## Authentication

All endpoints except `/auth/login`, `/books/stream`, and documentation endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer your-token-here
```

## Real-Time Updates

The `/books/stream` endpoint provides real-time updates when new books are created. Connect to this endpoint to receive Server-Sent Events with new book data.

## Development

This application requires Python 3.12 or higher.

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
uvicorn app.main:app --reload
```

3. Access the API documentation at:

-   Swagger UI: http://localhost:8000/docs
-   ReDoc: http://localhost:8000/redoc
