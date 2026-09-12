from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import Book, BookCreate
from services import book_service
from security import get_current_user, require_admin

router = APIRouter()

@router.post("/books", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db), user=Depends(require_admin)):
    return book_service.create_book(db, book)

@router.get("/books", response_model=List[Book])
def list_books(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return book_service.list_books(db)

@router.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return book_service.get_book(db, book_id)

@router.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db), user=Depends(require_admin)):
    return book_service.update_book(db, book_id, book)

@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    book_service.delete_book(db, book_id)
    return {"message": "Book deleted successfully"}
