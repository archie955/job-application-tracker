from fastapi import APIRouter, status, Depends, HTTPException
from server.models import models, schemas
from server.database.database import get_db
from sqlalchemy.orm import Session
from server.utils import utils

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate,
                db: Session = Depends(get_db)
                ):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"This email is already used"
                            )
    user.password = utils.hash(user.password)
    
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user