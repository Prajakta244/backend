from sqlalchemy import Column, Integer, String,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Syllabus(Base):
    __tablename__ = 'syllabus'
    id = Column(Integer, primary_key=True, index=True)
    year = Column(String)
    course = Column(String)
    degree = Column(Integer)
    filepath = Column(String)
    syllabus_year = Column(Integer)

class Reference_books(Base):
    __tablename__ = 'reference_books'
    id = Column(Integer, primary_key=True, index=True)
    year = Column(String)
    course = Column(String)
    degree = Column(Integer)
    filepath = Column(String)
    subject = Column(String) 
    semester = Column(String)    

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    is_admin = Column(String)
