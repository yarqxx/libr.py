from sqlalchemy.orm import Session
import models, schemas


def create_author(db: Session, author: schemas.Author):
    db_author = models.Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def create_user(db: Session, user: schemas.User):
    db_user = models.User(login=user.login, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_book(db: Session, book: schemas.Book, author_name: str):
    author_id = get_author_by_name(db, author_name).id
    db_book = models.Book(title=book.title,
                          text=book.text,
                          author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.login == username).first()


def get_author_by_name(db: Session, name: str):
    return db.query(models.Author).filter(models.Author.name == name).first()


def get_book_by_title(db: Session, title: str):
    return db.query(models.Book).filter(models.Book.title == title).first()


def get_books_by_author_name(db: Session, name: str):
    if author := get_author_by_name(db, name):
        return author.books
    return None
