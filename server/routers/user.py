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
    hashed_password = utils.hash(user.password)
    
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return schemas.UserOut(id=new_user.id, email=new_user.email, created_at=new_user.created_at)

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

    return schemas.Token(access_token=access_token, token_type="bearer")


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(get_db),
                      current_user: models.User = Depends(auth.get_current_user)
                      ):

    db.delete(current_user)
    db.commit()

    return


@router.put("/me/email", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def update_user_email(new_email: schemas.UpdateEmail,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)
                ):
    same_email = utils.check_email(new_email.email,
                                   current_user.email
                                   )

    if same_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This is the same email"
                            )
    
    if db.query(models.User).filter(models.User.email == new_email.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This email is already in use"
                            )

    current_user.email = new_email.email

    db.commit()

    return schemas.UserOut(id=current_user.id, email=new_email, created_at=current_user.created_at)

@router.put("/me/password", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def update_user_password(new_password: schemas.UpdatePassword,
                         db: Session = Depends(get_db),
                         current_user: models.User = Depends(auth.get_current_user)
                         ):
    same_password = utils.verify(new_password.password,
                                 current_user.hashed_password
                                 )

    if same_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This is the same password"
                            )
    
    current_user.hashed_password = utils.hash(new_password.password)

    db.commit()

    return schemas.UserOut(id=current_user.id, email=current_user.email, created_at=current_user.created_at)

