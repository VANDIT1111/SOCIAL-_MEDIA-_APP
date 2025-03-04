from fastapi import APIRouter, Depends, HTTPException, Response, status 
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from app import models, schemas, oauth2
from app.database import get_db
from pydantic import BaseModel, ConfigDict

router = APIRouter(tags=['POST'])


from app.schemas import PostResponse  # Use the correct model

class PostWithVotes(BaseModel):
    post: PostResponse  # Reference the renamed model correctly
    votes: int


    model_config = ConfigDict(from_attributes=True)

@router.get("/", response_model=List[schemas.PostWithVotes])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""):
    
    query = db.query(models.Post)
    
    if search:
        query = query.filter(models.Post.title.contains(search))  
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
                .outerjoin(models.Vote, models.Vote.post_id == models.Post.id) \
                .group_by(models.Post.id) \
                .offset(skip) \
                .limit(limit) \
                .all()
    
    return [
        PostWithVotes(post=PostResponse.from_orm(post), votes=votes)
        for post, votes in results
    ]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)):
   
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action" )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostResponse)
def update_post(
    id: int, 
    updated_post: schemas.PostCreate, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)):
   
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist")
        
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    updated_post = post_query.first()  
    return updated_post
