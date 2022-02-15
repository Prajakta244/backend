from typing import List
from fastapi import FastAPI,Depends,status,Response,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.sql.expression import true
import app.models as models
from app.database import engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.routers import syllabus,user,authentication,reference_book


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.include_router(authentication.router)
app.include_router(syllabus.router)
app.include_router(reference_book.router)
app.include_router(user.router)
app.include_router(authentication.router)

models.Base.metadata.create_all(engine)





