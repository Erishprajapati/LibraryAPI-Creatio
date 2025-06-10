from pydantic import BaseModel
class Book(BaseModel):
    title:str
    description:str
    author:str
    published_date:int

class showBook(Book):
    class Config():
        from_attributes = True

class SavedBook(BaseModel):
    book_id: int

class ShowSavedBook(BaseModel):
    id: int
    book_id: int
    book: showBook
    
    class Config():
        from_attributes = True

class User(BaseModel):
    name:str
    email:str
    password:str

class UpdateUserProfile(BaseModel):
    name: str
    email: str

class LoginUser(BaseModel):
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str