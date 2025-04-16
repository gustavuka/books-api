from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api import auth, books, users

app = FastAPI(
    title="Book Management API",
    description="A FastAPI application for managing books with authentication",
    version="1.0.0",
    swagger_ui_parameters={
        "persistAuthorization": True,
        "defaultModelsExpandDepth": -1,  # Hide schemas by default
    },
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(books.router, prefix="/books", tags=["books"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Book Management API"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Book Management API",
        version="1.0.0",
        description="A FastAPI application for managing books with authentication",
        routes=app.routes,
    )

    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token (without 'Bearer ' prefix)",
        }
    }

    # Apply security to all paths except public ones
    paths = openapi_schema.get("paths", {})
    for path in paths:
        if path not in [
            "/",
            "/users",
            "/auth/login",
            "/docs",
            "/openapi.json",
            "/redoc",
        ]:
            for method in paths[path]:
                if method != "options":
                    paths[path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
