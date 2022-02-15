from fastapi import APIRouter, Depends,HTTPException,status,Response
from sqlalchemy.orm import session
from app import schemas,models,database,hashing

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.post('/')
def create_user(request:schemas.User,db:session = Depends(database.get_db)):
    hashedPassword = hashing.Hash.bcrypt(request.password)
    new_user = models.User(name=request.name,email=request.email,password=hashedPassword,is_admin=request.is_admin)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',response_model=schemas.User)
def get_user(id,db:session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with id {id} not found')
    return user

@router.delete('/{id}')
def getSyllabus(id,db: session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with id {id} not found')
    else:
        user.delete(synchronize_session=False)
        db.commit()

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request: schemas.User,response : Response,db: session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with id {id} not found') 
    else:
        hashedPassword = hashing.Hash.bcrypt(request.password)
        db.query(models.User).filter(models.User.id == id).update({'name':request.name,'email':request.email,'password':hashedPassword,'is_admin':request.is_admin})
        db.commit()
        db.refresh(user)
    return {'status':'success','updated user':user}
