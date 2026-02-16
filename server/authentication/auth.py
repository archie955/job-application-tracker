import jwt
from fastapi.security import OAuth2PasswordBearer
from server.utils.config import settings
from datetime import datetime, timezone, timedelta
from server.models.schemas import Token, TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = str(payload.get("user_id"))

        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id=id)
        return token_data
    
    except jwt.exceptions.InvalidTokenError:
        raise credentials_exception
    
