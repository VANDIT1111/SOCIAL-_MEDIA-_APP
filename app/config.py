from pydantic_settings import BaseSettings
from dotenv import load_dotenv

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1111@localhost:5432/fastapi"


load_dotenv()

SECRET_KEY = "settings.secrect_key"

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str  
    secret_key: str  
    algorithm: str
    access_token_expire_minutes: int
    DATABASE_URL: str
  

    class Config:
        env_file = ".env"  

settings = Settings()


print(settings.dict()) 

