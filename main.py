# from fastapi import FastAPI
# from typing import Optional
# from pydantic import BaseModel
# app = FastAPI()
# @app.get('/')
# def home(limit =  10, published:bool = True):
#     """messages are sent in key value pair for now to check"""
#     if published:
#         return {'data': f'{limit} books shown from Library Management System'}
#     else:
#         return None

# @app.get('/home/unpublished')
# def unpublished_books():
#     return {'data' : "List of unpublished books:"}

# @app.get('/about')
# def about_page():
#     return {'data' : "Welcome to about section"}

# @app.get('/home/{book_id}')
# def specific_book(book_id:int): #to get specific book with the id
#     return {'data':12} 

# @app.get('/home/{book_id}/comments')
# def comments(book_id:int, limit = 10): #type hinting to make id as integer to pass integer only
#     return {'data': {'1','2','3'}} 

# class Book(BaseModel):
#     title:str
#     description: str
#     author : str
#     published_date: Optional[bool]

# @app.post('/library')
# def add_book(request: Book):
#     return {'data' : f'Book have been added as Name:{request.title} by Author: {request.author}'}

from fastapi import FastAPI, Depends
import models,schemas
from database import engine, SessionLocal
import schemas  
from sqlalchemy.orm import Session
app = FastAPI()
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/')
def create(request: schemas.Book, db:Session = Depends(get_db)):
    new_book = models.Book(title=request.title, description = request.description)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book