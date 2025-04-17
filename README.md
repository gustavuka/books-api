# Book Management API

A FastAPI-based REST API for managing a collection of books with real-time updates.

## Features

-   User authentication with JWT tokens
-   CRUD operations for books
-   Real-time updates using Server-Sent Events (SSE)
-   Pagination support
-   Search functionality

## Deployment

The application is deployed on Heroku at [https://gustavo-books-api-8453f37cfc3a.herokuapp.com/](https://gustavo-books-api-8453f37cfc3a.herokuapp.com/).

### Database Configuration

-   Locally it works with SQLite
-   The deployed application uses PostgreSQL on Heroku instead of SQLite. SQLite is not recommended for production use on Heroku due to its file-based nature and limitations with Heroku's ephemeral filesystem

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

## Using the API Documentation (Swagger UI)

-   Run the application locally and access http://localhost:8000/docs
-   The API documentation is also available at [https://gustavo-books-api-8453f37cfc3a.herokuapp.com/docs](https://gustavo-books-api-8453f37cfc3a.herokuapp.com/docs).

1. **Create a User Account**

    - Click on the `POST /users/` endpoint
    - Click "Try it out"
    - Enter your user details in the request body:
        ```json
        {
            "username": "yourusername",
            "email": "your@email.com",
            "password": "yourpassword"
        }
        ```
    - Click "Execute"

2. **Login and Get Token**

    - Click on the `POST /auth/login` endpoint
    - Click "Try it out"
    - Enter your credentials:
        ```json
        {
            "username": "yourusername",
            "password": "yourpassword"
        }
        ```
    - Click "Execute"
    - Copy the `access_token` from the response

3. **Authorize the API**

    - Click the "Authorize" button at the top of the page
    - Enter your token in the format: `your-token-here`
    - Click "Authorize"
    - Now you can use all protected endpoints

4. **Using Protected Endpoints**

    - Try creating a book with `POST /books/`
    - List books with `GET /books/`
    - Update or delete books using their IDs
