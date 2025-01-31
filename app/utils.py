from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
import random
import aiosmtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  
SMTP_USERNAME = os.getenv("vanditdudhatra207@gmail.com")  
SMTP_PASSWORD = os.getenv("jwfw sisp nwzq xqwg")  

async def send_email_otp(email: str, otp: str):
    message = EmailMessage()
    message["From"] = SMTP_USERNAME
    message["To"] = email
    message["Subject"] = "Your OTP Code"
    message.set_content(f"Your OTP code is: {otp}")

    try:
        await aiosmtplib.send(
            message,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD,
            start_tls=True,  
        )
        return {"message": "OTP sent successfully"}
    except Exception as e:
        return {"error": f"Failed to send OTP: {str(e)}"}



def hash(password: str):
    return pwd_context.hash(password) 


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)