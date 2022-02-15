from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile,File


class SchemaSyllabus(BaseModel):
    year: str
    course: str
    degree: str
    syllabus_year:int

    class Config:
        orm_mode = True

class SchemaBook(BaseModel):
    year: str
    semester: str
    degree: str
    

    class Config:
        orm_mode = True        

class User(BaseModel):
    name : str
    email : str
    password : str
    is_admin : str

    class Config:
        orm_mode = True

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None 