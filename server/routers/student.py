from .. import schemas
from .. import models
from .. import utils
from fastapi import  FastAPI,Response,status, HTTPException,Depends,APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session


router = APIRouter(tags=['Student'])

@router.post("/student")
def student_post(student:schemas.RequestStudent,db:Session = Depends(get_db)):
    hashed_password = utils.hash(student.password)
    student.password = hashed_password
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return "test"

@router.get("/student/{id}",response_model=schemas.ResponseStudent)
def student_get(id: int, db:Session = Depends(get_db)):
    data = db.query(models.Student).filter(models.Student.id == id).first()
    return data

@router.put("/student/{id}")
def make_admin(id: int,db:Session = Depends(get_db)):
    student_query = db.query(models.Student).filter(models.Student.id == id)
    student = student_query.first()
    student.role = "ADMIN"
    print(student.role)
    db.commit()
    return student_query.first()

@router.delete("/student/{id}")
def delete_student(id: int,db:Session = Depends(get_db)):
    student_query = db.query(models.Student).filter(models.Student.id == id)
    student =student_query.first()
    if student == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"student with id: {id} does not exist")
    student_query.delete(synchronize_session=False)
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)
#Update request for student to make its spaces private to public