from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

# --- POST MODELS ---
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):  # Avoid duplicate "Post" naming conflicts
    id: int
    created_at: datetime
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

class PostWithVotes(BaseModel):
    post: PostResponse  
    votes: int

    model_config = ConfigDict(from_attributes=True)

# --- USER MODELS ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# --- TOKEN MODELS ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# --- VOTE MODEL ---
class Vote(BaseModel):
    post_id: int
    dir: int  

# --- OTP VERIFICATION MODEL ---
class OTPVerification(BaseModel):
    email: EmailStr
    otp: str

# --- LOGIN REQUEST MODEL ---
class LoginRequest(BaseModel):
    email: str
    password: str

# --- LIKE MODELS ---
class LikeCreate(BaseModel):
    post_id: int

class LikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- COMMENT MODELS ---
class CommentCreate(BaseModel):
    post_id: int
    content: str

class CommentResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CommentLikeCreate(BaseModel):
    comment_id: int

class CommentLikeResponse(BaseModel):
    id: int
    user_id: int
    comment_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
