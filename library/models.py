from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    books = relationship("Book", back_populates="parent")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True)
    password = Column(String)


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    text = Column(String)
    author_id = Column(Integer, ForeignKey('author.id'))
    parent = relationship("Author", back_populates='books')