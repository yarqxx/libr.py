from pydantic import BaseModel
from typing import List, Optional, Type
import models


class Author(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Book(BaseModel):
    title: str

    class Config:
        orm_mode = True


class CreateBook(Book):
    text: str


class User(BaseModel):
    login: str
    password: str

