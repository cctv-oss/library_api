from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
from schemas import BookCreate
from repositories import book_repo

def create_book(db: Session, book: BookCreate):
    data = book.model_dump()
    data["available"] = data["total_stock"]   # 业务规则:新书全部可借
    return book_repo.create_book(db, data)

def list_books(db: Session):
    return book_repo.list_books(db)

def get_book(db: Session, book_id: int):
    book = book_repo.get_book(db, book_id)
    if book is None:                            # 业务判断:不存在
        raise HTTPException(status_code=404, detail="Book not found")
    return book

def update_book(db: Session, book_id: int, book: BookCreate):
    db_book = book_repo.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    borrowed = db_book.total_stock - db_book.available   # 业务:借出数不变
    data = book.model_dump()
    data["available"] = data["total_stock"] - borrowed
    return book_repo.update_book(db, db_book, data)

def delete_book(db: Session, book_id: int):
    book = book_repo.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    # 检查是否还有借阅记录,有则不允许删除
    has_borrow = db.query(models.BorrowRecords).filter(
        models.BorrowRecords.book_id == book_id
    ).count() > 0
    if has_borrow:
        raise HTTPException(status_code=400, detail="该图书有借阅记录,无法删除")
    book_repo.delete_book(db, book)
