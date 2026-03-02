from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime
from models.datatypes import AssessmentType, ApplicationStatus


config = ConfigDict(from_attributes=True)

# Token model

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]




# User schemas

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = config
    id: int
    email: EmailStr
    created_at: datetime


class UserDelete(BaseModel):
    detail: str

class UpdateEmail(BaseModel):
    email: EmailStr

class UpdatePassword(BaseModel):
    password: str




# jobs + assessments schemas


class Job(BaseModel):
    model_config = config
    employer: str
    title: str
    status: Optional[ApplicationStatus] = ApplicationStatus.NOT_APPLIED
    description: Optional[str] = None
    location: str
    deadline: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class JobComplete(Job):
    model_config = config
    user_id: int
    id: int



class Assessment(BaseModel):
    model_config = config
    job_id: int
    id: int
    type: AssessmentType
    description: str
    completed: bool
    deadline: Optional[datetime] = None


class JobDetail(JobComplete):
    assessments: Optional[List[Assessment]] = None


