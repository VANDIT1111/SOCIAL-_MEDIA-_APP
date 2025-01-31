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
    fastmail_smtp_server: str
    fastmail_smtp_port: int
    fastmail_username: str
    fastmail_password: str

    class Config:
        env_file = ".env"  

settings = Settings()


print(settings.dict()) 

class Config:
    SECRET_KEY = 'your_secret_key_here'
    SECURITY_PASSWORD_SALT = 'your_salt_here'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your_email@gmail.com'
    MAIL_PASSWORD = 'your_email_password'
    BASE_URL = 'http://localhost:5000'

