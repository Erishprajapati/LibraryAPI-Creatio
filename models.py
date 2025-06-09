from database import Base
from sqlalchemy import Column,String,Integer

class Book(Base):
    __tablename__ = "books"  # <-- Required!

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)

class User(Base):
    __tablename__ = 'Userss'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

