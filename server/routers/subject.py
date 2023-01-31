from .. import schemas
from .. import models
from .. import utils
from fastapi import  FastAPI,Response,status, HTTPException,Depends,APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(tags=['Subject'])

@router.post('/subject')
def add_subject(subject: schemas.RequestSubject,db: Session = Depends(get_db)):
    new_subject = models.Subject(**subject.dict())
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject

#get request
@router.get('/subject')
def get_all_subject(db: Session = Depends(get_db)):
    subject = db.query(models.Subject).all()
    return subject

@router.get('/subject/{sem}')
def get_subject_by_sem(sem:int, db: Session = Depends(get_db)):
    subject = db.query(models.Subject).filter(models.Subject.sem_id == sem).all()
    return subject

@router.delete('/subject/{id}')
def delete_subject_by_id(id:int,  db: Session = Depends(get_db)):
    subject_query = db.query(models.Subject).filter(models.Subject.id == id)
    subject = subject_query.first()
    if subject == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"subject with id: {id} does not exist")

    subject_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/subject/{id}')
def update_subject_by_id(id:int,data: schemas.RequestSubject,db: Session = Depends(get_db)):
    subject_query = db.query(models.Subject).filter(models.Subject.id == id)
    subject = subject_query.first()
    if subject == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"subject with id: {id} does not exist")
    subject_query.update(data.dict(),synchronize_session=False)
    db.commit()
    return subject_query.first() 