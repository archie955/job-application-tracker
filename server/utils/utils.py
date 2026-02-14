from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


if __name__ == "__main__":
    hashed_pwd = hash(settings.database_password)
    print(verify(settings.database_password, hashed_pwd))