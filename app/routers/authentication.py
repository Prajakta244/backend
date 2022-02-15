from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from app import database,schemas,models,jwttoken
from app.hashing import Hash
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/login')
def login(req:OAuth2PasswordRequestForm =  Depends(), db: Session = Depends(database.get_db)):
    user =  db.query(models.User).filter(models.User.email == req.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Invalid Credentials.')
    if not Hash.verify_hash(req.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Invalid password.')
    access_token = jwttoken.create_access_token(data = {"sub":user.email})
    return {"access_token": access_token, "token_type": "bearer"}