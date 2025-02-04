from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, func, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    
    owner = relationship("User", back_populates="posts")

    
    votes = relationship('Vote', back_populates='post', cascade="all, delete-orphan")



followers_table = Table(
    'followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('following_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    otp = Column(String, nullable=True)
    verified = Column(Boolean, default=False)
    otp_expires_at = Column(DateTime, nullable=True)  
    created_at = Column(DateTime, default=datetime.utcnow)

    
    posts = relationship("Post", back_populates="owner")

    
    following = relationship(
        'User',
        secondary=followers_table,
        primaryjoin=id == followers_table.c.follower_id,
        secondaryjoin=id == followers_table.c.following_id,
        backref='followers'
    )



class Vote(Base):
    __tablename__ = 'votes'

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"))  
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

    
    post = relationship('Post', back_populates='votes')



class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CommentLike(Base):
    __tablename__ = 'comment_likes'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    comment_id = Column(Integer, ForeignKey('comments.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    
class UserProfile(BaseModel):
    username: str
    email: str