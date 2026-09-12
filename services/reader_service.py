from sqlalchemy.orm import Session
from fastapi import HTTPException
import models
from repositories import reader_repo
from schemas import ReaderCreate
from security import hash_password


def create_reader(db: Session, reader: ReaderCreate):
    data = reader.model_dump()
    password = data.pop("password", None) or "123456"   # 没填密码就默认 123456
    data["password_hash"] = hash_password(password)      # 存加密后的密码
    return reader_repo.create_reader(db, data)

def list_readers(db: Session):
    return reader_repo.list_reader(db)

def search_reader(db: Session, keyword: str):
    return reader_repo.search_reader(db, keyword)

def get_reader(db: Session, reader_id: int):
    reader = reader_repo.get_reader( db, reader_id)
    if reader is None:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader

def update_reader(db: Session, reader: ReaderCreate, reader_id: int):
    db_reader = reader_repo.get_reader(db, reader_id)
    if db_reader is None:
        raise HTTPException(status_code=404, detail="Reader not found")
    data = reader.model_dump()
    password = data.pop("password", None)
    if password:  # 只有填了新密码才更新
        db_reader.password_hash = hash_password(password)
    return reader_repo.update_reader(db, db_reader, data)

def delete_reader(db: Session, reader_id: int):
    reader = reader_repo.get_reader(db, reader_id)
    if reader is None:
        raise HTTPException(status_code=404, detail="Reader not found")
    # 检查是否还有借阅记录,有则不允许删除
    has_borrow = db.query(models.BorrowRecords).filter(
        models.BorrowRecords.reader_id == reader_id
    ).count() > 0
    if has_borrow:
        raise HTTPException(status_code=400, detail="该读者有借阅记录,无法删除")
    reader_repo.delete_reader(db, reader)
