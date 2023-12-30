from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2
from typing import Annotated
from database import LocalSession, engine
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import models
import schemas
import crud

SECRET_KEY = "19109197bd5e7c289b92b2b355083ea26c71dee2085ceccc19308a7291b2ea06"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


@app.post('/token_get')
def token_get(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user_data = crud.get_user(db, username=form_data.username)
    if not user_data:
        raise HTTPException(status_code=400, detail="Incorrect username")
    else:
        if not pwd_context.verify(form_data.password, user_data.password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        token = hash_password(data={"sub": user_data.username})

    return {"access_token": token, "token_type": "bearer"}


def hash_password(data: dict):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post('/token_create')
def token_create(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user_data = crud.get_user(db, username=form_data.username)
    if user_data:
        raise HTTPException(status_code=400, detail="This username already existed")

    form_data.password = hash_password({'password': form_data.password})

    crud.create_user(db, user=schemas.User(login=form_data.username, password=form_data.password))
    return {"access_token": form_data.username, "token_type": "bearer"}


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.Author, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db, name=author.name)
    if db_author:
        return HTTPException(status_code=400, detail="User already exists")
    db_author = crud.create_author(db, author=author)
    return db_author


@app.get("/author/{author_name}/")
def get_author_books(author_name: str, db: Session = Depends(get_db)):
    db_books = crud.get_books_by_author_name(db, name=author_name)
    return db_books


@app.get("/{title}/")
def get_book(title: str, db: Session = Depends(get_db)):
    db_books = crud.get_book_by_title(db, title=title)
    return db_books


@app.post("/{author_name}/", response_model=schemas.Book)
def create_book(book: schemas.CreateBook, author_name: str, db: Session = Depends(get_db)):
    db_author = crud.create_book(db, book=book, author_name=author_name)
    return db_author

