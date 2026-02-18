from sqlalchemy import String, ForeignKey, DateTime, Text, func, Enum as sqlEnum, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from datetime import datetime
from ..database.database import Base
from .datatypes import AssessmentType, ApplicationStatus

application_status = sqlEnum(ApplicationStatus, name="application_status")
assessment_type = sqlEnum(AssessmentType, name="assessment_type")

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True,
                                    nullable=False
                                    )
    email: Mapped[str] = mapped_column(String(100),
                                       unique=True,
                                       nullable=False,
                                       index=True
                                       )
    hashed_password: Mapped[str] = mapped_column(String(200),
                                          nullable=False
                                          )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now()
                                                 )
    hashed_refresh_token: Mapped[str] = mapped_column(Text,
                                                      nullable=True
                                                      )
    jobs: Mapped[List["Job"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    

    

class Job(Base):
    __tablename__ = "jobs"
    __table_args__ = (
        UniqueConstraint("user_id", "employer", "title"),

    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),
                                         nullable=False,
                                         index=True
                                         )
    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True,
                                    nullable=False
                                    )
    
    employer: Mapped[str] = mapped_column(String(200),
                                          nullable=False
                                          )
    title: Mapped[str] = mapped_column(String(200),
                                       nullable=False
                                       )
    status: Mapped[ApplicationStatus] = mapped_column(application_status,
                                                       nullable=False,
                                                       default=ApplicationStatus.NOT_APPLIED
                                                       )
    description: Mapped[str] = mapped_column(Text,
                                             nullable=True
                                             )
    location: Mapped[str] = mapped_column(String(200),
                                          nullable=False
                                          )
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                               nullable=True
                                               )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now()
                                                 )
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now()
                                                 )
    
    user: Mapped["User"] = relationship(
        back_populates="jobs"
    )
    assessments: Mapped[List["Assessment"]] = relationship(
        back_populates="job",
        cascade="all, delete-orphan"
    )
    
class Assessment(Base):
    __tablename__ = "assessments"

    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"),
                                        nullable=False,
                                        index=True
                                        )
    id: Mapped[int] = mapped_column(primary_key=True,
                                    nullable=False,
                                    autoincrement=True
                                    )
    type: Mapped[AssessmentType] = mapped_column(assessment_type,
                                                 nullable=False
                                                 )
    description: Mapped[str] = mapped_column(Text,
                                             nullable=True
                                             )
    completed: Mapped[bool] = mapped_column(nullable=False,
                                            default=False
                                            )
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                               nullable=True
                                               )
    job: Mapped["Job"] = relationship(
        back_populates="assessments"
    )
    
    