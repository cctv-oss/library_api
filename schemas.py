from datetime import date
from typing import Optional

from pydantic import BaseModel , Field


class BookCreate(BaseModel):
    title : str
    author : str
    price : float= 0.00
    total_stock : int = 0
    available : int = 0
    publish : Optional[date]=None
    introduction : Optional[str]=None

class Book(BaseModel):
    id:int
    title : str
    author : str
    price : float
    total_stock : int
    available : int
    publish : Optional[date]
    introduction : Optional[str]

    model_config = {"from_attributes":True}

class ReaderCreate(BaseModel):
    name : str
    phone : str
    email : Optional[str]=None
    reg_date : date = Field(default_factory = date.today)
    status : int = 1
    password : Optional[str] = None   # 登录密码(不填则默认 123456)

class Reader(BaseModel):
    id: int
    name: str
    phone : str
    email : Optional[str]
    reg_date : date
    status : int
    model_config = {"from_attributes":True}

class BorrowCreate(BaseModel):
    reader_id : int
    book_id : int

class Borrow(BaseModel):
    id: int
    reader_id : int
    book_id : int
    borrow_date : date
    due_date : date
    return_date : Optional[date]
    status : str
    model_config = {"from_attributes":True}


class LoginRequest(BaseModel):
    account : str    # 管理员填用户名,读者填手机号
    password : str
    role : str       # "admin" 或 "reader"


class TokenResponse(BaseModel):
    token : str
    role : str
    id : int
    name : str


class ReaderBorrowCreate(BaseModel):
    book_id : int

