

from sqlalchemy.orm import Session

import models
from models import Readers
from sqlalchemy import or_


def create_reader(db: Session, data: dict):
    reader = Readers(**data)
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader

def list_reader(db: Session):
    return db.query(Readers).all()

def search_reader(db: Session, keyword: str):
    return db.query(Readers).filter(
        or_(
            Readers.name.like(f"%{keyword}%"),
            Readers.phone.like(f"%{keyword}%"),
        )
    ).all()

def get_reader(db: Session,reader_id: int):
    return db.query(Readers).filter(Readers.id == reader_id).first()

def update_reader(db: Session, reader: models.Readers, data: dict):
    reader.name = data["name"]
    reader.phone = data["phone"]
    reader.email = data["email"]
    reader.status = data["status"]
    db.commit()
    db.refresh(reader)
    return reader

def delete_reader(db: Session, reader: models.Readers):
    db.delete(reader)
    db.commit()
