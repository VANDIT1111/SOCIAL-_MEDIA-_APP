import logging
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.models import User, UserProfile
from app.database import get_db

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

router = APIRouter(tags=['PROFILE'])

@router.get("/profile/{username}", response_model=UserProfile)
async def view_profile(username: str, db: Session = Depends(get_db)):
    logging.info(f"Fetching profile for username: {username}")

    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        logging.warning(f"User {username} not found")
        raise HTTPException(status_code=404, detail="User not found")

    logging.info(f"Profile fetched successfully for {username}")
    return user

@router.put("/profile/{username}", response_model=UserProfile)
async def edit_profile(username: str, user_profile: UserProfile, db: Session = Depends(get_db)):
    logging.info(f"Updating profile for username: {username}")

    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        logging.warning(f"User {username} not found for update")
        raise HTTPException(status_code=404, detail="User not found")

    user.username = user_profile.username
    user.email = user_profile.email

    db.commit()
    logging.info(f"Profile updated for {username}")

    return user_profile
