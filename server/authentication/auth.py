import jwt
from fastapi.security import OAuth2PasswordBearer
from server.utils.config import settings
from datetime import datetime, timezone, timedelta
from server.models.schemas import Token, TokenData
from fastapi import Depends, HTTPException, status
from server.database.database import get_db
from sqlalchemy.orm import Session
import server.models.models as models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days
CREDENTIALS_EXCEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="Could not validate credentials",
                                      headers={"WWW-Authenticate": "Bearer"}
                                      )

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})

    encoded_jwt = jwt.encode(to_encode,
                             SECRET_KEY,
                             algorithm=ALGORITHM
                             )

    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})

    encoded_jwt = jwt.encode(to_encode,
                             SECRET_KEY,
                             algorithm=ALGORITHM
                             )
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token,
                             SECRET_KEY,
                             algorithms=[ALGORITHM]
                             )
        return payload
    except jwt.exceptions.InvalidTokenError:
        raise CREDENTIALS_EXCEPTION


def verify_access_token(token: str
                        ):
    payload = decode_token(token)

    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token type"
                            )
    
    user_id = str(payload.get("sub"))

    if not user_id:
        raise CREDENTIALS_EXCEPTION
    
    return TokenData(id=user_id)
    
def get_current_user(token: str = Depends(oauth2_scheme), 
                     db: Session = Depends(get_db)
                     ):
    user_id_token = verify_access_token(token=token
                                )

    user = db.query(models.User).filter(models.User.id == user_id_token.id).first()

    if not user:
        raise CREDENTIALS_EXCEPTION
    
    return user