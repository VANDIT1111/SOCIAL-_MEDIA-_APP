from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

from pydantic.types import conint

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
    
class Vote(BaseModel):
    post_id: int
    dir: int  
    
class OTPVerification(BaseModel):
    email: EmailStr
    otp: str
    
    
class LoginRequest(BaseModel):
    email: str
    password: str