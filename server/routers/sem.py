from fastapi import  APIRouter, FastAPI,Response,status, HTTPException,Depends
from sqlalchemy.orm import Session
from ..database import engine, get_db
from pydantic import BaseModel
from typing import List
from .. import schemas,Oauth2
from .. import models

router = APIRouter(tags=['SEM'])


@router.post("/sem")
def add_sem(sem:schemas.RequestSem ,db:Session = Depends(get_db)):
    new_sem = models.Sem(**sem.dict()) 
    db.add(new_sem)
    db.commit()
    db.refresh(new_sem)
    return new_sem

@router.get("/sem",response_model=List[schemas.ResponseSem])
def get_all_sem(db: Session = Depends(get_db)):
    sems = db.query(models.Sem).all()
    return {"sems": sems}

@router.get("/sem/{id}", response_model=schemas.ResponseSem)
def get_sem_by_id(id: int,db: Session = Depends(get_db)):
    sem = db.query(models.Sem).filter(models.Sem.id == id)
    sem_data = sem.first()
    if sem_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"sem with id: {id} does not exist")
    return sem_data

@router.put("/sem/{id}", response_model=schemas.ResponseSem)
def update_sem_by_id(id: int, sem: schemas.RequestSem, db: Session = Depends(get_db)):
    sem_query = db.query(models.Sem).filter(models.Sem.id == id)
    sem_data = sem_query.first()
    sem_query.update(sem.dict(),synchronize_session=False)
    db.commit()
    return sem_query.first()

@router.delete("/sem/{id}")
def delete_sem_by_id(id: int,db: Session = Depends(get_db)):
    sem_query = db.query(models.Sem).filter(models.Sem.id == id)
    sem_data = sem_query.first()
    if sem_data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"sem with id: {id} does not exist")
    
    sem_query.delete(synchronize_session=False) 
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)