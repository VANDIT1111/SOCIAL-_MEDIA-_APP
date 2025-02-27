import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

print("✅ Updated PYTHONPATH:", sys.path)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app import models
from app.database import engine
from passlib.context import CryptContext
from app.routers import post, like_comment, auth, vote, follow, profile
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App is starting...")  # Startup actions here
    yield
    print("App is shutting down...")  # Shutdown actions here

# Use a single FastAPI instance
fastapi_app = FastAPI(lifespan=lifespan)

# Include routers
fastapi_app.include_router(post.router)
fastapi_app.include_router(like_comment.router)
fastapi_app.include_router(auth.router)
fastapi_app.include_router(vote.router)
fastapi_app.include_router(follow.router)
fastapi_app.include_router(profile.router)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("🚀 Application is starting...")

if __name__ == "__main__":
    print("✅ App started!")
