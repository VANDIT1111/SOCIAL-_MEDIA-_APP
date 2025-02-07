from fastapi import FastAPI
from app import models
from app.database import engine
from passlib.context import CryptContext
from app.routers import post, like_comment, auth, vote, follow, profile

fastapi_app = FastAPI()


fastapi_app.include_router(post.router)
fastapi_app.include_router(like_comment.router)
fastapi_app.include_router(auth.router)
fastapi_app.include_router(vote.router)
fastapi_app.include_router(follow.router)
fastapi_app.include_router(profile.router)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@fastapi_app.on_event("startup")
def on_startup():
    print("FastAPI app started. Creating database tables...")
   
    models.Base.metadata.create_all(bind=engine)
    
  



