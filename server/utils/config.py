from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int


    class Config:
        env_file = ".env"

settings = Settings()