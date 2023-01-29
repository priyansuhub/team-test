from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database,models,schemas,utils,Oauth2


router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(student_credentials:OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(database.get_db)):
    student = db.query(models.Student).filter(models.Student.email == student_credentials.username).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Galat EMail")
    
    if not utils.compareHash(student_credentials.password, student.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email or Password")

    access_token = Oauth2.create_access_token(data={"student_id": student.id, "role":student.role})

    return {"access_token": access_token}