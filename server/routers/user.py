from fastapi import APIRouter, status, Depends, HTTPException
from server.models import models, schemas
from server.database.database import get_db
from sqlalchemy.orm import Session
from server.utils import utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from server.authentication import auth

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,
                db: Session = Depends(get_db)
                ):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This email is already used"
                            )
    user.password = utils.hash(user.password)
    
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)
                ):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Username or Password"
                            )
    if not utils.verify(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Username or Password"
                            )
    
    access_token = auth.create_access_token(data = {"user_id": user.id})

    response_object = schemas.Token(access_token=access_token,
                                    token_type="bearer"
                                    )

    return response_object


@router.delete("/delete/{current_user.id}", status_code=status.HTTP_200_OK, response_model=schemas.UserDelete)
def delete_user(db: Session = Depends(get_db),
                      current_user: models.User = Depends(auth.get_current_user)
                      ):

    db.delete(current_user)
    db.commit()
    db.refresh()

    response_object = schemas.UserDelete(deleted="successfully deleted",
                                         user=current_user
                                         )

    return response_object


# @router.put("/update/{current_user.id}")