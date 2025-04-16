from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, description="Title cannot be empty")
    author: str = Field(..., min_length=1, description="Author cannot be empty")
    published_date: date
    summary: Optional[str] = None
    genre: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(
        None, min_length=1, description="Title cannot be empty"
    )
    author: Optional[str] = Field(
        None, min_length=1, description="Author cannot be empty"
    )
    published_date: Optional[date] = None
    summary: Optional[str] = None
    genre: Optional[str] = None


class Book(BookBase):
    id: int

    class Config:
        from_attributes = True


class PaginatedBooks(BaseModel):
    total: int
    skip: int
    limit: int
    books: List[Book]
