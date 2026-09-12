from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from schemas import Reader, ReaderCreate
from services import reader_service
from security import require_admin

router = APIRouter()

@router.post("/readers",response_model=Reader)
def create_reader(reader: ReaderCreate, db: Session = Depends(get_db), user=Depends(require_admin)):
    return reader_service.create_reader(db, reader)

@router.get("/readers",response_model=List[Reader])
def list_readers(db: Session = Depends(get_db), user=Depends(require_admin)):
    return reader_service.list_readers(db)

@router.get("/readers/search",response_model=List[Reader])
def search_reader(keyword: str, db: Session = Depends(get_db), user=Depends(require_admin)):
    return reader_service.search_reader(db, keyword)

@router.get("/readers/{reader_id}",response_model=Reader)
def get_reader(reader_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    return reader_service.get_reader(db, reader_id)

@router.put("/readers/{reader_id}",response_model=Reader)
def update_reader(reader_id: int, reader: ReaderCreate, db: Session = Depends(get_db), user=Depends(require_admin)):
    return reader_service.update_reader(db, reader, reader_id)

@router.delete("/readers/{reader_id}")
def delete_reader(reader_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    reader_service.delete_reader(db, reader_id)
    return {"message": "Reader deleted successfully"}
