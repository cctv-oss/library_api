from datetime import date
from typing import Optional

from pydantic import BaseModel

class BookCreate(BaseModel):
    title : str
    author : str
    price : float= 0.00
    stock : int = 0
    publish : Optional[date]=None
    introduction : Optional[str]=None

class Book(BaseModel):
    id:int
    title : str
    author : str
    price : float
    stock : int
    publish : Optional[date]
    introduction : Optional[str]

    model_config = {"from_attributes":True}