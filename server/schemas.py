from typing import Optional
from pydantic import BaseModel, EmailStr

class TokenData(BaseModel):
    id: Optional[str] = None
    role: Optional[str] = None

class RequestStudent(BaseModel):
    email:EmailStr
    password:str

class ResponseStudent(BaseModel):
    email:EmailStr
    public:bool

    class Config:
        orm_mode = True

class RequestSem(BaseModel):
    semnum: str

class ResponseSem(BaseModel):
    semnum: str
        
    class Config:
        orm_mode = True

class RequestSubject(BaseModel):
    subject_code: str
    sem_id: int

class RequestQuestion(BaseModel):
    question:str
    answer:str
    image:Optional[str] = None
    priority:str
    subject_id:int

class RequestSpace(BaseModel):
    subject:str
    question:str
    answer:str
    image:Optional[str]=None
    priority:Optional[str]=None
    user_id:int