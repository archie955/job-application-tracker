from pydantic_settings import BaseSettings
from pydantic import ConfigDict


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
    vite_baseurl: str
    frontend_url: str
    backend_url: str
    nginx_baseurl: str
    model_config = ConfigDict(env_file=".env")



settings = Settings()