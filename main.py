from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import engine, Base, SessionLocal
from schemas import Book, BookCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books", response_model=Book)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = models.Books(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books", response_model=List[Book])
async def list_books(db: Session = Depends(get_db)):
    return db.query(models.Books).all()

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        return book

@app.put("/books/{book_id}", response_model=Book)
async def change_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        db_book.title = book.title
        db_book.author = book.author
        db_book.price = book.price
        db_book.stock = book.stock
        db_book.publish = book.publish
        db_book.introduction = book.introduction
        db.commit()
        db.refresh(db_book)
        return db_book
@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        db.delete(book)
        db.commit()
        return { "message": "Book deleted successfully" }

