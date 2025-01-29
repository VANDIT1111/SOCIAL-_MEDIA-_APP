from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import post, user, auth, vote  
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:Vd11-11-@localhost:5432/fastapi"


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


for route in app.routes:
    print(route.path, route.methods)


@app.get("/")
def root():
    return {"message": "Hello, Welcome To My API"}
