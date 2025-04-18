import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.events import event_manager
from app.core.security import get_current_user
from app.database.database import get_db
from app.models.book import Book
from app.schemas.book import Book as BookSchema
from app.schemas.book import BookCreate, BookUpdate, PaginatedBooks

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/stream")
async def stream_books():
    return StreamingResponse(
        event_manager.subscribe(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@router.get("/", response_model=PaginatedBooks)
async def list_books(
    skip: int = Query(0, ge=0, description="Skip N records"),
    limit: int = Query(20, ge=1, le=100, description="Limit to N records"),
    db: Session = Depends(get_db),
):
    total = db.query(Book).count()
    books = db.query(Book).offset(skip).limit(limit).all()
    return PaginatedBooks(books=books, total=total, skip=skip, limit=limit)


@router.get("/{book_id}", response_model=BookSchema)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return book


@router.post("/", response_model=BookSchema)
async def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    # Convert the book to a dict and ensure the date is serializable
    book_data = BookSchema.from_orm(db_book).dict()
    book_data["published_date"] = book_data["published_date"].isoformat()

    # Broadcast the new book to all connected clients
    asyncio.create_task(
        event_manager.broadcast(
            json.dumps({"event": "book_created", "data": book_data})
        )
    )

    return db_book


@router.patch("/{book_id}", response_model=BookSchema)
async def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db),
):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )

    # Update only the fields that are provided
    for field, value in book_update.model_dump(exclude_unset=True).items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    db.delete(db_book)
    db.commit()
    return None
