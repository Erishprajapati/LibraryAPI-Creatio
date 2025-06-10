from pydantic import BaseModel
class Book(BaseModel):
    title:str
    description:str

class showBook(Book):
    class Config():
        from_attributes = True


class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str