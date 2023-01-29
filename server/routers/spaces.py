from .. import schemas
from .. import models
from .. import utils
from fastapi import  FastAPI,Response,status, HTTPException,Depends,APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(tags=['Spaces'])

@router.post("/spaces")
def post_public_spaces(spaces:schemas.RequestSpace, db:Session = Depends(get_db)):
    new_space = models.Spaces(**spaces.dict()) 
    db.add(new_space)
    db.commit()
    db.refresh(new_space)
    return new_space

@router.get("/spaces/available")
def get_space_profiles(db:Session = Depends(get_db)):
    data = db.query(models.Spaces).filter(models.Spaces.public == 'TRUE').all()
    return data

@router.get("/space/{id}")
def get_space_by_id(id: int,db:Session = Depends(get_db)):
    data = db.query(models.Spaces).filter(models.Spaces.id == id).first()
    return data

@router.put("/space/{id}")
def update_space_by_id(id: int, spaces:schemas.RequestSpace,db:Session = Depends(get_db)):
    space_query = db.query(models.Spaces).filter(models.Student.id == id)
    space = space_query.first()
    if space == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Space with id: {id} does not exist")
    space_query.update(spaces.dict(),synchronize_session=False)
    db.commit()
    return space_query.filter()

@router.delete("/space/{id}")
def delete_spaces_by_id(id: int,db: Session = Depends(get_db)):
    space_query = db.query(models.Spaces).filter(models.Student.id == id)
    space = space_query.first()
    if space == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"space with id: {id} does not exist")
    
    space_query.delete(synchronize_session=False) 
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)