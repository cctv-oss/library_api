from datetime import date

from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, Numeric, Date, Text, ForeignKey

from database import Base


class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(100),nullable=False)
    author = Column(String(50),nullable=False)
    price = Column(Numeric(10,2),nullable=False,default=0.00)
    total_stock = Column(Integer,nullable=False,default=0)
    available = Column(Integer,nullable=False,default=0)
    publish = Column(Date)
    introduction = Column(Text)

class Readers(Base):
    __tablename__ = 'readers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50),nullable=False)
    phone = Column(String(50),nullable=False,unique=True)
    email = Column(String(50))
    reg_date = Column(Date,nullable=False,default=date.today)
    status = Column(Integer,nullable=False,default=1)
    password_hash = Column(String(200), default='')  # 登录密码(加密存储,不存明文)

class BorrowRecords(Base):
    __tablename__ = 'borrow_records'
    id = Column(Integer, primary_key=True)
    reader_id = Column(Integer,ForeignKey('readers.id'),nullable=False)
    book_id = Column(Integer,ForeignKey('books.id'),nullable=False)
    borrow_date = Column(Date,nullable=False)
    due_date = Column(Date,nullable=False)
    return_date = Column(Date)
    status = Column(String(20),nullable=False,default='borrowed')
    reader = relationship("Readers")
    book = relationship("Books")


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(200), nullable=False)