from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timezone
from server.models.datatypes import AssessmentType, ApplicationStatus

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
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class UserDelete(BaseModel):
    detail: str

class UpdateEmail(BaseModel):
    email: EmailStr

class UpdatePassword(BaseModel):
    password: str




# jobs + assessments schemas

class Job(BaseModel):
    employer: str
    title: str
    status: Optional[ApplicationStatus] = ApplicationStatus.NOT_APPLIED
    description: Optional[str] = None
    location: str
    deadline: Optional[datetime] = None
    created_at: Optional[datetime] = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = datetime.now(timezone.utc)

    class Config:
        from_attributes = True

class JobCreate(Job):
    user_id: int
    
class JobComplete(JobCreate):
    id: int

class Assessment(BaseModel):
    job_id: int
    id: int
    type: AssessmentType
    description: str
    completed: bool
    deadline: datetime

class JobDetail(BaseModel):
    job: JobComplete
    assessments: Optional[List[Assessment]] = None


