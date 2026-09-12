from datetime import date, timedelta

from sqlalchemy.orm import Session
from fastapi import HTTPException
from repositories import reader_repo, book_repo, borrow_repo


def borrow(db:Session,book_id:int,reader_id:int):
    reader = reader_repo.get_reader(db, reader_id)
    if reader is None:
        raise HTTPException(status_code=404, detail="Reader not found")
    if reader.status !=1:
        raise HTTPException(status_code=400, detail="Reader not active")
    book = book_repo.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.available <=0:
        raise HTTPException(status_code=400, detail="Book not available")
    active = borrow_repo.count_active_borrows(db, reader_id)
    if active >= 3:
        raise HTTPException(status_code=400, detail="Reader has borrowed 3 books")
    book.available -= 1
    data = {
        "book_id": book_id,
        "reader_id": reader_id,
        "borrow_date": date.today(),
        "due_date": date.today()+timedelta(days=14),
        "status": "borrowed"
    }
    return borrow_repo.create_borrow(db, data)

def return_book(db: Session, borrow_id:int):
        record = borrow_repo.get_borrow(db, borrow_id)
        if record is None:
            raise HTTPException(status_code=404, detail="Borrow record not found")
        if record.status != "borrowed":
            raise HTTPException(status_code=400, detail="Book is returned")
        book = book_repo.get_book(db, record.book_id)
        book.available += 1
        record.return_date = date.today()
        record.status = "overdue" if record.due_date < record.return_date else "returned"
        return borrow_repo.return_borrow(db, record)

def list_borrows(db: Session, reader_id:int=None,status:str=None):
    return borrow_repo.list_borrows(db,reader_id,status)
