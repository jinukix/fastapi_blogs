from fastapi import FastAPI

from app.database import engine, Base, get_db
from routers import blog, user

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)
