from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from repositories import borrow_repo
from schemas import Borrow, ReaderBorrowCreate
from security import require_reader
from services import borrow_service

router = APIRouter()


@router.get("/me/borrows", response_model=List[Borrow])
def my_borrows(user=Depends(require_reader), db: Session = Depends(get_db)):
    """读者查看自己的借阅记录"""
    return borrow_service.list_borrows(db, reader_id=user["id"])


@router.post("/me/borrow", response_model=Borrow)
def my_borrow(data: ReaderBorrowCreate, user=Depends(require_reader), db: Session = Depends(get_db)):
    """读者自己借书(reader_id 从登录身份取,不用自己传)"""
    return borrow_service.borrow(db, data.book_id, user["id"])


@router.post("/me/borrows/{borrow_id}/return", response_model=Borrow)
def my_return(borrow_id: int, user=Depends(require_reader), db: Session = Depends(get_db)):
    """读者归还自己的书"""
    record = borrow_repo.get_borrow(db, borrow_id)
    if record is None or record.reader_id != user["id"]:
        raise HTTPException(status_code=403, detail="只能归还自己的借阅记录")
    return borrow_service.return_book(db, borrow_id)
