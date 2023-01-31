from fastapi import  APIRouter, FastAPI,Response,status, HTTPException,Depends
from sqlalchemy.orm import Session
from ..database import engine, get_db
from pydantic import BaseModel
from typing import List
from .. import schemas,Oauth2
from .. import models

router = APIRouter(tags=['Questions'])

# create
@router.post("/question")
def add_question(question:schemas.RequestQuestion,db: Session = Depends(get_db),current_user = Depends(Oauth2.get_current_user)):
    if(current_user.role != "ADMIN"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")
    new_ques = models.Question(**question.dict())
    db.add(new_ques)
    db.commit()
    db.refresh(new_ques)
    return new_ques

@router.get('/question')
def get_all_question(db: Session = Depends(get_db), current_user = Depends(Oauth2.get_current_user)):
    print(current_user.role)
    if(current_user.role != "ADMIN"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")
    subject = db.query(models.Question).all()
    return {"subject":subject}

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdHVkZW50X2lkIjoyLCJyb2xlIjoiVVNFUiIsImV4cCI6MTY3NTE1ODczOH0.hO9KliAUb3nOyKO95tSQL_VJnVrVoAjK-IqZ7BD1f7I
@router.get("/question/{id}")
def get_question_by_id(id: int,db: Session = Depends(get_db)):
    subject = db.query(models.Question).filter(models.Subject.id)
    subject_data = subject.first()
    if subject_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"sem with id: {id} does not exist")
    return subject_data

@router.put("/question/{id}")
def update_question_by_id(id: int, question: schemas.RequestQuestion, db: Session = Depends(get_db)):
    question_query = db.query(models.Question).filter(models.Question.id == id)
    question_data = question_query.first()
    question_query.update(question.dict(),synchronize_session=False)
    db.commit()
    return question_query.first()

@router.delete("/question/{id}")
def delete_question_by_id(id: int,db: Session = Depends(get_db)):
    question_query = db.query(models.Question).filter(models.Question.id == id)
    question_data = question_query.first()
    if question_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"question with id: {id} does not exist")
    
    question_query.delete(synchronize_session=False) 
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)