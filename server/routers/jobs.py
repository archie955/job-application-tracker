from fastapi import APIRouter, HTTPException, status, Depends
from models import models, schemas
from sqlalchemy.orm import Session
from database.database import get_db
from authentication.auth import get_current_user
from typing import List
from models.datatypes import ApplicationStatus
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["Jobs"])



@router.post("/create", status_code=status.HTTP_200_OK, response_model=schemas.JobComplete)
def create_job(job: schemas.Job,
               db: Session = Depends(get_db),
               user: models.User = Depends(get_current_user)
               ):
    logger.info("Job creation attempt", extra={"user_id": user.id, "employer": job.employer, "title": job.title})
    new_job = models.Job(user_id=user.id, **job.model_dump())

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    logger.info("Successful job creation", extra={"user_id": user.id, "employer": job.employer, "title": job.title})
    return schemas.JobComplete.model_validate(new_job)



@router.get("/get", status_code=status.HTTP_200_OK, response_model=List[schemas.JobDetail])
def get_jobs(db: Session = Depends(get_db),
             user: models.User = Depends(get_current_user),
             limit: int = 10,
             skip: int = 0
             ):
    logger.info("Get jobs request", extra={"user_id": user.id})
    jobs = db.query(models.Job).filter(models.Job.user_id == user.id)\
           .order_by(models.Job.updated_at.desc()).limit(limit).offset(skip).all()
    
    res = [schemas.JobDetail(id=job.id,
                             user_id=job.user_id,
                             employer=job.employer,
                             title=job.title,
                             description=job.description,
                             status=job.status,
                             location=job.location,
                             deadline=job.deadline,
                             created_at=job.created_at,
                             updated_at=job.updated_at,
                             assessments=job.assessments) for job in jobs]
    
    logger.info("Successful get jobs request", extra={"user_id": user.id})
    
    return res



@router.get("/get/{id}", status_code=status.HTTP_200_OK, response_model=schemas.JobDetail)
def get_job(id: int,
            db: Session = Depends(get_db),
            user: models.User = Depends(get_current_user),
            ):
    job = db.query(models.Job).filter(models.Job.user_id == user.id,
                                      models.Job.id == id).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    logger.info("Get single job request", extra={"user_id": user.id, "employer": job.employer, "title": job.title})
    res = schemas.JobDetail(id=job.id,
                             user_id=job.user_id,
                             employer=job.employer,
                             title=job.title,
                             description=job.description,
                             location=job.location,
                             deadline=job.deadline,
                             created_at=job.created_at,
                             updated_at=job.updated_at,
                             assessments=job.assessments)
    
    logger.info("Successful get single job request", extra={"user_id": user.id, "employer": job.employer, "title": job.title})

    return res
    


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(id: int,
               db: Session = Depends(get_db),
               user: models.User = Depends(get_current_user)
               ):
    logger.info("Delete job request", extra={"user_id": user.id, "job_id": id})    

    job = db.query(models.Job).filter(models.Job.user_id == user.id,
                                      models.Job.id == id).first()

    if not job:
        logger.warning("Failed delete job request", extra={"user_id": user.id, "job_id": id})
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Job not found"
                            )
    db.delete(job)
    db.commit()

    logger.info("Successful delete job request", extra={"user_id": user.id, "job_id": id})

    return



@router.put("/update/{id}", status_code=status.HTTP_200_OK, response_model=schemas.JobComplete)
def update_job(id: int,
               new_job_info: schemas.Job,
               db: Session = Depends(get_db),
               user: models.User = Depends(get_current_user)
               ):
    logger.info("Update job request", extra={"user_id": user.id, "job_id": id})

    job = db.query(models.Job).filter(models.Job.user_id == user.id,
                                      models.Job.id == id).first()
    if not job:
        logger.warning("Failed job update request", extra={"user_id": user.id, "job_id": id})
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Job not found"
                            )
    job.employer = new_job_info.employer
    job.title = new_job_info.title
    job.status = new_job_info.status
    job.description = new_job_info.description
    job.location = new_job_info.location
    job.deadline = new_job_info.deadline

    db.commit()
    db.refresh(job)

    logger.info("Successful update job request", extra={"user_id": user.id, "job_id": id})

    return schemas.JobComplete.model_validate(job)



@router.get("/get/not_applied", status_code=status.HTTP_200_OK, response_model=List[schemas.JobDetail])
def get_not_applied_jobs(db: Session = Depends(get_db),
                         user: models.User = Depends(get_current_user)
                         ):
    jobs = db.query(models.Job).filter(models.Job.user_id == user.id,
                                       models.Job.status == ApplicationStatus.NOT_APPLIED)\
                                       .order_by(models.Job.deadline).all()
    res = [schemas.JobDetail(id=job.id,
                             user_id=job.user_id,
                             employer=job.employer,
                             title=job.title,
                             description=job.description,
                             location=job.location,
                             deadline=job.deadline,
                             created_at=job.created_at,
                             updated_at=job.updated_at,
                             assessments=job.assessments) for job in jobs]

    return res



@router.get("/get/deadlines", status_code=status.HTTP_200_OK, response_model=List[schemas.JobDetail])
def get_applied_jobs(db: Session = Depends(get_db),
                     user: models.User = Depends(get_current_user)
                     ):
    jobs = db.query(models.Job).filter(models.Job.user_id == user.id,
                                       models.Job.status != ApplicationStatus.NOT_APPLIED)\
                                       .all()
    res = [schemas.JobDetail(id=job.id,
                             user_id=job.user_id,
                             employer=job.employer,
                             title=job.title,
                             description=job.description,
                             location=job.location,
                             deadline=job.deadline,
                             created_at=job.created_at,
                             updated_at=job.updated_at,
                             assessments=job.assessments) for job in jobs]
    
    return res


