from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Book(Base):
    __tablename__ = "books"  # <-- Required!

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    author = Column(String)
    published_date = Column(Integer)
    
    # Relationship
    saved_by = relationship("SavedBook", back_populates="book")

class User(Base):
    __tablename__ = 'Userss'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    
    # Relationship
    saved_books = relationship("SavedBook", back_populates="user")

class SavedBook(Base):
    __tablename__ = 'saved_books'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('Userss.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    
    # Relationships
    user = relationship("User", back_populates="saved_books")
    book = relationship("Book", back_populates="saved_by")
# Revert table name Wed Jun 11 09:50:42 +0545 2025
