from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, oauth2
from app.database import get_db
from app.schemas import CommentLikeCreate, CommentLikeResponse
from app.oauth2 import get_current_user
from app.models import User, Comment, CommentLike

router = APIRouter(tags=['LIKE/COMMENT']

)


@router.post("/like/", response_model=schemas.LikeResponse)
def like_post(
    like: schemas.LikeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
   
    post_id = like.post_id  

   
    new_like = models.Like(user_id=current_user.id, post_id=post_id)

    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like


@router.post("/comment/", response_model=schemas.CommentResponse)
def add_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_comment = Comment(
        user_id=current_user.id,  
        post_id=comment.post_id,
        content=comment.content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment



@router.post("/comment/like/", response_model=CommentLikeResponse)
def like_comment(
    comment_like: CommentLikeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_comment_like = CommentLike(
        user_id=current_user.id,  
        comment_id=comment_like.comment_id
    )
    db.add(new_comment_like)
    db.commit()
    db.refresh(new_comment_like)
    return new_comment_like


