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

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,
                             SECRET_KEY,
                             algorithm=ALGORITHM
                             )

    return encoded_jwt

def verify_access_token(token: str,
                        credentials_exception
                        ):
    try:
        payload = jwt.decode(token,
                             SECRET_KEY, 
                             algorithms=[ALGORITHM]
                             )
        id: str = payload.get("sub")

        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id=id)
        return token_data
    
    except jwt.exceptions.InvalidTokenError:
        raise credentials_exception
    
async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: Session = Depends(get_db)
                           ):
    credentials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail=f"Could not validate credentials",
                                           headers={"WWW-Authenticate": "Bearer"}
                                           )
    token = verify_access_token(token,
                                credentials_exception=credentials_exceptions
                                )

    user = db.query(models.User).filter(models.User.id == token.id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"User does not exist"
                            )
    
    return user