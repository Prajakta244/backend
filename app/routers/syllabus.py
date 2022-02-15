from fastapi import APIRouter, Depends,HTTPException,status,Response,File,UploadFile
from pydantic.types import FilePath
from sqlalchemy.orm import session
from app import schemas,models,database,oauth2
import os


router = APIRouter(
    prefix='/syllabus',
    tags=['Syllabus']
)

@router.post('/')
def createSyllabus(filepath: UploadFile = File(...),degree: str = File(...),course: str = File(...),year: str = File(...),syllabus_year: str = File(...),db: session = Depends(database.get_db)):
    if not os.path.exists(f"C:/website/frontend/public/assets/uploads/syllabus/{course}/{degree}/{year}"):
        os.makedirs(f"C:/website/frontend/public/assets/uploads/syllabus/{course}/{degree}/{year}")
    print(f"C:/website/frontend/public/assets/uploads/syllabus/{course}/{degree}/{year}/{filepath.filename}")
    file_location = f"C:/website/frontend/public/assets/uploads/syllabus/{course}/{degree}/{year}/{filepath.filename}"
    assetFilePath = f"/assets/uploads/syllabus/{course}/{degree}/{year}/{filepath.filename}"
    # year: str,course: str,degree: str,
    # with open(filepath.filename, 'w') as file:
    #     file.write(filepath)
    with open(file_location, "wb+") as file_object:
        file_object.write(filepath.file.read())
    new_syllabus = models.Syllabus(year=year,course=course,degree=degree,filepath=assetFilePath,syllabus_year=syllabus_year)
    db.add(new_syllabus)
    db.commit()
    db.refresh(new_syllabus)
    return new_syllabus
    return True

@router.get('/')
def getAllSyllabus(db: session = Depends(database.get_db)):
    syllabus = db.query(models.Syllabus).all()
    return syllabus

@router.get('/{syllabus_year}')
def getSyllabus(syllabus_year,db: session = Depends(database.get_db)):
    syllabus = db.query(models.Syllabus).filter(models.Syllabus.syllabus_year == syllabus_year).first()
    if not syllabus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Syllabus with syllabus_year {syllabus_year} not found')
    return syllabus

@router.post('/filter_syllabus')
def filter_syllabus(request:schemas.SchemaSyllabus,db: session = Depends(database.get_db)):
    print('request',request)
    syllabus = db.query(models.Syllabus).filter(models.Syllabus.syllabus_year == request.syllabus_year,models.Syllabus.degree == request.degree,models.Syllabus.course == request.course,models.Syllabus.year == request.year).first()
    # query.filter(User.name == 'ed', User.fullname == 'Ed Jones')
    if not syllabus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Syllabus with syllabus_year {request.syllabus_year} not found')
    return syllabus

@router.delete('/{id}')
def getSyllabus(id,db: session = Depends(database.get_db)):
    syllabus = db.query(models.Syllabus).filter(models.Syllabus.id == id)
    if not syllabus.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Syllabus with id {id} not found')
    else:
        syllabus.delete(synchronize_session=False)
        db.commit()

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request: schemas.SchemaSyllabus,response : Response,db: session = Depends(database.get_db)):
    syllabus = db.query(models.Syllabus).filter(models.Syllabus.id == id).first()
    if not syllabus:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Syllabus with id {id} not found') 
    else:
        db.query(models.Syllabus).filter(models.Syllabus.id == id).update(dict(request))
        db.commit()
        db.refresh(syllabus)
    return {'status':'success','updated syllabus':syllabus}