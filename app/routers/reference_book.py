from fastapi import APIRouter, Depends,HTTPException,status,Response,File,UploadFile
from pydantic.types import FilePath
from sqlalchemy.orm import session
from app import schemas,models,database,oauth2
import os


router = APIRouter(
    prefix='/reference_book',
    tags=['Reference_book']
)

@router.post('/')
def createReference_book(filepath: UploadFile = File(...),degree: str = File(...),course: str = File(...),year: str = File(...),subject: str = File(...),db: session = Depends(database.get_db)):
    if not os.path.exists(f"C:/website/frontend/public/assets/uploads/reference_books/{course}/{degree}/{year}"):
        os.makedirs(f"C:/website/frontend/public/assets/uploads/reference_books/{course}/{degree}/{year}")
    print(f"C:/website/frontend/public/assets/uploads/reference_books/{course}/{degree}/{year}/{filepath.filename}")
    file_location = f"C:/website/frontend/public/assets/uploads/reference_books/{course}/{degree}/{year}/{filepath.filename}"
    assetFilePath = f"/assets/uploads/reference_books/{course}/{degree}/{year}/{filepath.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(filepath.file.read())
    new_syllabus = models.Reference_books(year=year,course=course,degree=degree,filepath=assetFilePath,subject=subject)
    db.add(new_syllabus)
    db.commit()
    db.refresh(new_syllabus)
    return new_syllabus
    return True

@router.get('/')
def getAllReference_book(db: session = Depends(database.get_db)):
    reference_books = db.query(models.Reference_books).all()
    return reference_books

@router.get('/{syllabus_year}')
def getReference_book(syllabus_year,db: session = Depends(database.get_db)):
    reference_books = db.query(models.Reference_books).filter(models.Reference_books.syllabus_year == syllabus_year).first()
    if not reference_books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Reference_books with syllabus_year {syllabus_year} not found')
    return reference_books

@router.post('/filter_books')
def filter_books(request:schemas.SchemaBook,db: session = Depends(database.get_db)):
    print('request',request)
    reference_books = db.query(models.Reference_books).filter(models.Reference_books.year == request.year,models.Reference_books.degree == request.degree,models.Reference_books.semester == request.semester).all()
    # query.filter(User.name == 'ed', User.fullname == 'Ed Jones')
    if not reference_books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Reference_books for  {request.semester} not found')
    return reference_books

@router.delete('/{id}')
def getReference_book(id,db: session = Depends(database.get_db)):
    reference_books = db.query(models.Reference_books).filter(models.Reference_books.id == id)
    if not reference_books.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Reference_books with id {id} not found')
    else:
        reference_books.delete(synchronize_session=False)
        db.commit()

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request: schemas.SchemaSyllabus,response : Response,db: session = Depends(database.get_db)):
    reference_books = db.query(models.Reference_books).filter(models.Reference_books.id == id).first()
    if not reference_books:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Reference_books with id {id} not found') 
    else:
        db.query(models.Reference_books).filter(models.Reference_books.id == id).update(dict(request))
        db.commit()
        db.refresh(reference_books)
    return {'status':'success','updated reference_books':reference_books}