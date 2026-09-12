from sqlalchemy.orm import Session
import models

def create_book(db: Session, data: dict):
    book = models.Books(**data)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def list_books(db: Session):
    return db.query(models.Books).all()

def get_book(db: Session, book_id: int):
    return db.query(models.Books).filter(models.Books.id == book_id).first()

def update_book(db: Session, book: models.Books, data: dict):
    book.title = data["title"]
    book.author = data["author"]
    book.price = data["price"]
    book.publish = data["publish"]
    book.introduction = data["introduction"]
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book: models.Books):
    db.delete(book)
    db.commit()