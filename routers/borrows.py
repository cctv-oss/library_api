from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import Borrow, BorrowCreate
from services import borrow_service
from security import require_admin

router = APIRouter()

@router.post("/borrow",response_model=Borrow)
def borrow ( data:BorrowCreate, db: Session = Depends(get_db), user=Depends(require_admin)):
    return borrow_service.borrow(db, data.book_id, data.reader_id)

@router.post("/borrows/{borrow_id}/return",response_model=Borrow)
def return_book ( borrow_id:int, db: Session = Depends(get_db), user=Depends(require_admin)):
    return borrow_service.return_book(db, borrow_id)

@router.get("/borrows", response_model=List[Borrow])
def list_borrows(reader_id: int=None , status: str=None , db: Session = Depends(get_db), user=Depends(require_admin)):
    return borrow_service.list_borrows(db, reader_id, status)
