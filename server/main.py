from .database import engine, get_db
from . import models
from fastapi import  APIRouter, FastAPI,Response,status, HTTPException,Depends
from .routers import student
from .routers import question
from .routers import auth
from .routers import subject
from .routers import sem

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
# app.include_router(question.router)
app.include_router(student.router)
app.include_router(auth.router)
app.include_router(question.router)
app.include_router(subject.router)
app.include_router(sem.router)

