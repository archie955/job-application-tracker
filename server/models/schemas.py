from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

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
