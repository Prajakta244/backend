from fastapi import FastAPI,Depends,HTTPException,status,Request,Response
from . import schemas,models,database,hashing
from sqlalchemy.orm import session
from sqlalchemy import and_
import json

models.Base.metadata.create_all(database.engine)

app = FastAPI()





