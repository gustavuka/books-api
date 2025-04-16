from sqlalchemy import Column, Date, Integer, String

from app.database.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    published_date = Column(Date)
    summary = Column(String)
    genre = Column(String)
