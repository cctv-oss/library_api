from sqlalchemy.orm import Session
import models

def count_active_borrows(db: Session, reader_id: int):
    return db.query(models.BorrowRecords).filter(
        models.BorrowRecords.reader_id == reader_id,
        models.BorrowRecords.status == 'borrowed'
    ).count()

def create_borrow(db: Session, data:dict):
    record = models.BorrowRecords(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_borrow(db: Session, borrow_id: int):
    return db.query(models.BorrowRecords).filter(models.BorrowRecords.id == borrow_id).first()

def return_borrow(db: Session, record: models.BorrowRecords):
    db.commit()
    db.refresh(record)
    return record

def list_borrows(db, reader_id=None, status=None):
    q = db.query(models.BorrowRecords)
    if reader_id is not None:
        q = q.filter(models.BorrowRecords.reader_id == reader_id)
    if status is not None:
        q = q.filter(models.BorrowRecords.status == status)
    return q.all()