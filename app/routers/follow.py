from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.oauth2 import get_current_user


router = APIRouter(
    prefix="/follow",
    tags=["Follow"]
)

@router.post("/{user_id}", status_code=status.HTTP_200_OK)
def follow_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself.")
    
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found.")

    if target_user in current_user.following:
        raise HTTPException(status_code=400, detail="You are already following this user.")

    current_user.following.append(target_user)
    db.commit()
    return {"message": f"You are now following {target_user.username}"}



@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def unfollow_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found.")

    if target_user not in current_user.following:
        raise HTTPException(status_code=400, detail="You are not following this user.")

    current_user.following.remove(target_user)
    db.commit()
    return {"message": f"You have unfollowed {target_user.username}"}
