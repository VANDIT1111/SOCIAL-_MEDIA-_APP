from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    


class PostCreate(PostBase):
    pass

class Post(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True
        from_attributes = True
        

class PostWithVotes(BaseModel):
    post: Post  
    votes: int

    class Config:
        orm_mode = True 
        from_attributes = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class PostOut(PostBase):
    Post: Post
    votes: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
    
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    
    
class Vote(BaseModel):
    post_id: int
    dir: int  
    
class OTPVerification(BaseModel):
    email: EmailStr
    otp: str
    
    
class LoginRequest(BaseModel):
    email: str
    password: str
    
    
    
class LikeCreate(BaseModel):
    post_id: int
    
    
class LikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    post_id: int
    content: str


class CommentResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True


class CommentLikeCreate(BaseModel):
    comment_id: int

class CommentLikeResponse(BaseModel):
    id: int
    user_id: int
    comment_id: int
    created_at: datetime

    class Config:
        orm_mode = True