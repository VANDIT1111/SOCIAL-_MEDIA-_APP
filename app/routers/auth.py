import random
import bcrypt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
from app import schemas
from app import models
from app import oauth2
from app.database import get_db
from app.models import User, Like, Comment, CommentLike
from app.utils import  send_email_otp
from app.oauth2 import SECRET_KEY, ALGORITHM, get_current_user
from app.schemas import OTPVerification, LoginRequest, LikeCreate, LikeResponse, CommentCreate, CommentResponse, CommentLikeCreate, CommentLikeResponse, TokenResponse


from app.models import User

router = APIRouter(tags=['USER AUTHENTICATION'])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/create", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    
    hashed_password = oauth2.hash_password(user.password)  

  
    new_user = models.User(email=user.email, password=hashed_password)

   
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), ):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail=f"User with id: {id} does not exist")
                           

    return user


@router.post("/register")
async def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    otp = str(random.randint(100000, 999999))
    otp_expires_at = datetime.utcnow() + timedelta(minutes=2)  

    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        otp=otp,
        otp_expires_at=otp_expires_at,  
        verified=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    await send_email_otp(email, otp)

    return {"message": "User registered successfully. Please verify OTP."}


@router.post("/verify-otp")
async def verify_otp(otp_request: OTPVerification, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == otp_request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.otp or user.otp != otp_request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if user.otp_expires_at and user.otp_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired. Please request a new one.")

    user.verified = True
    user.otp = None  
    user.otp_expires_at = None
    db.commit()

    return {"message": "Account verified successfully"}


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
   
    user = db.query(User).filter(User.email == request.email).first()

   
    if not user or not bcrypt.checkpw(request.password.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=400, detail="Invalid credentials")

 
    if not user.verified:
        raise HTTPException(status_code=403, detail="Account not verified. Please verify OTP.")

    
    token = jwt.encode(
        {"user_id": user.id, "exp": datetime.utcnow() + timedelta(hours=2)},
        SECRET_KEY,
        algorithm="HS256",
    )

   
    print(f"Generated Token: {token}")


    return {"access_token": token, "token_type": "bearer"}

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    new_password: str

def send_reset_email(email: str, reset_token: str):
    """Send the reset link to the user's email (you can replace this with an email service)."""
    print(f"Sending reset email to {email} with token: {reset_token}")


@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    email = request.email
    user = db.query(User).filter_by(email=email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    reset_token = jwt.encode({
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, SECRET_KEY, algorithm=ALGORITHM)

    send_reset_email(email, reset_token)

    return {"message": "Password reset link has been sent to your email"}


@router.post("/reset-password/{token}")
async def reset_password(token: str, request: ResetPasswordRequest, db: Session = Depends(get_db)):
    new_password = request.new_password

    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = decoded_data['email']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="The reset token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

 
    hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    user.password_hash = hashed_password
    db.commit()

    return {"message": "Password has been reset successfully"}












