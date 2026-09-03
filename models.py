from sqlalchemy import Column, Integer, String, Numeric, Date, Text

from database import Base


class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(100),nullable=False)
    author = Column(String(50),nullable=False)
    price = Column(Numeric(10,2),nullable=False,default=0.00)
    stock = Column(Integer,nullable=False,default=0)
    publish = Column(Date)
    introduction = Column(Text)