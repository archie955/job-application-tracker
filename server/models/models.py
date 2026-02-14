from sqlalchemy import Column, String, ForeignKey, DateTime, text, Text, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from datetime import datetime
from ..database.database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True,
                                    nullable=False)
    email: Mapped[str] = mapped_column(String(100),
                                       unique=True,
                                       nullable=False)
    password: Mapped[str] = mapped_column(String(200),
                                          nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now())
    

class Jobs(Base):
    __tablename__ = "jobs"


    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True,
                                    nullable=False)
    
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    
    