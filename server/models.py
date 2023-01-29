from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, Column, ForeignKey,Integer, String, Boolean,Text
from sqlalchemy.sql.expression import text

class Sem(Base):
    __tablename__ = "sem"
    id = Column(Integer,primary_key=True, nullable = False)
    semnum = Column(String, nullable=False)

class Subject(Base):
    __tablename__  = "subject"
    id = Column(Integer,primary_key=True, nullable = False)
    subject_code = Column(String, nullable=False)
    sem_id = Column(Integer, ForeignKey("sem.id", ondelete="CASCADE"), nullable=False)
    sem = relationship("Sem")

class Question(Base):
    __tablename__ = "question"
    id = Column(Integer,primary_key=True, nullable = False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    image = Column(String)
    priority = Column(String, server_default='LOW', nullable=False)
    subject_id = Column(Integer, ForeignKey("subject.id", ondelete="CASCADE"), nullable=False)
    subject = relationship("Subject")

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer,primary_key=True, nullable = False)
    email = Column(String, nullable=False)
    role = Column(String,server_default='USER',nullable=False)
    password = Column(String, nullable=False)
    public = Column(Boolean,server_default='FALSE',nullable=False)

class Spaces(Base):
    __tablename__ = "spaces"
    id = Column(Integer,primary_key=True, nullable = False)
    subject =  Column(String,nullable = False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    image = Column(String)
    priority = Column(String, server_default='LOW', nullable=False)
    user_id = Column(Integer, ForeignKey("student.id", ondelete="CASCADE"), nullable=False)
    user = relationship("Student")