from fastapi import FastAPI, HTTPException, Depends, APIRouter
from app.models import User, UserProfile
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(tags=['PROFILE'])


@router.get("/profile/{username}", response_model=UserProfile)
async def view_profile(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.put("/profile/{username}", response_model=UserProfile)
async def edit_profile(username: str, user_profile: UserProfile, db: Session = Depends(get_db)):
   
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    
    user.username = user_profile.username
    user.email = user_profile.email

   
    db.commit()

    return user_profile