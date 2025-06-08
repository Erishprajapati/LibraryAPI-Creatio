from fastapi import FastAPI
from pydantic import BaseModel
class Book(BaseModel):
    title:str
    description:str
