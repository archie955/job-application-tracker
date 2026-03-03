from fastapi import APIRouter, status, Depends, HTTPException, Request
from models import models, schemas
from database.database import get_db
from sqlalchemy.orm import Session
from utils import utils
from utils.config import settings
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from authentication import auth
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,
                db: Session = Depends(get_db)
                ):
    logger.info("Registration attempt", extra={"email": user.email})

    if db.query(models.User).filter(models.User.email == user.email).first():
        logger.warning("Failed registration attempt", extra={"email": user.email})

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

    logger.info("Successful Registration attempt", extra={"email": user.email})

    return schemas.UserOut(id=new_user.id, email=new_user.email, created_at=new_user.created_at)



@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)
                ):
    logger.info("Login attempt", extra={"email": user_credentials.username})
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        logger.warning("Failed login attempt", extra={"email": user_credentials.username})

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Username or Password"
                            )
    if not utils.verify(user_credentials.password, user.hashed_password):
        logger.warning("Failed login attempt - incorrect password", extra={"email": user_credentials.username})

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Username or Password"
                            )
    
    access_token = auth.create_access_token(data = {"sub": str(user.id)})
    refresh_token = auth.create_refresh_token(data = {"sub": str(user.id)})

    user.hashed_refresh_token = utils.hash(refresh_token)
    db.commit()

    response = JSONResponse(
        content=schemas.Token(access_token=access_token, token_type="bearer").model_dump()
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.prod, # true in prod, false in dev
        samesite="strict" if settings.prod else "lax"
    )

    logger.info("Successful login attempt", extra={"email": user_credentials.username})

    return response



@router.get("/logout")
def logout(db: Session = Depends(get_db),
           user: models.User = Depends(auth.get_current_user)
           ):
    logger.info("Logout attempt", extra={"email": user.email})

    response = JSONResponse(
        content={"message": "successfully logged out"}
    )
    response.delete_cookie(key="refresh_token")

    user.hashed_refresh_token = None
    db.commit()

    logger.info("Successful logout attempt", extra={"email": user.email})

    return response



@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def refresh_token(request: Request,
                  db: Session = Depends(get_db)
                  ):
    logger.info("Attempting refresh")

    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        logger.warning("Missing refresh token")

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Missing refresh token"
                            )
    
    payload = auth.decode_token(refresh_token)

    if payload.get("type") != "refresh":
        logger.warning("Missing refresh token")

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token type"
                            )
    
    user_id = payload.get("sub")

    if user_id is None:
        logger.warning("No identified user for refresh")

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token payload"
                            )
    
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        logger.warning("Failed refresh attempt", extra={"email": user.email})

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found"
                            )

    if not utils.verify(refresh_token, user.hashed_refresh_token):
        logger.warning("Failed refresh attempt", extra={"email": user.email})

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid refresh token"
                            )
    
    new_refresh = auth.create_refresh_token({"sub": str(user.id)})
    user.hashed_refresh_token = utils.hash(new_refresh)
    db.commit()

    new_access = auth.create_access_token({"sub": str(user.id)})

    response = JSONResponse(
        content=schemas.Token(access_token=new_access, token_type="bearer").model_dump()
        )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=settings.prod, # true in prod
        samesite="strict" if settings.prod else "lax"
    )

    logger.info("Successful refresh attempt", extra={"email": user.email})

    return response



@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)
                ):
    logger.info("User delete attempt", extra={"email": current_user.email})

    db.delete(current_user)
    db.commit()

    logger.info("Successfully deleted user", extra={"email": current_user.email})
    return



@router.put("/me/email", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def update_user_email(new_email: schemas.UpdateEmail,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)
                ):
    logger.info("User update attempt", extra={"email": current_user.email})
    same_email = utils.check_email(new_email.email,
                                   current_user.email
                                   )

    if same_email:
        logger.warning("Failed user update attempt", extra={"email": current_user.email})

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This is the same email"
                            )
    
    if db.query(models.User).filter(models.User.email == new_email.email).first():
        logger.warning("Failed user update attempt", extra={"email": current_user.email})

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This email is already in use"
                            )

    current_user.email = new_email.email

    db.commit()

    logger.info("Successful user update attempt", extra={"email": current_user.email})

    return schemas.UserOut(id=current_user.id, email=new_email.email, created_at=current_user.created_at)



@router.put("/me/password", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def update_user_password(new_password: schemas.UpdatePassword,
                         db: Session = Depends(get_db),
                         current_user: models.User = Depends(auth.get_current_user)
                         ):
    logger.info("User update attempt", extra={"email": current_user.email})

    same_password = utils.verify(new_password.password,
                                 current_user.hashed_password
                                 )

    if same_password:
        logger.warning("Failed user update attempt", extra={"email": current_user.email})

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This is the same password"
                            )
    
    current_user.hashed_password = utils.hash(new_password.password)

    db.commit()

    logger.info("Successful user update attempt", extra={"email": current_user.email})

    return schemas.UserOut(id=current_user.id, email=current_user.email, created_at=current_user.created_at)

