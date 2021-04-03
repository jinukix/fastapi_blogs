from fastapi import FastAPI

from app.database import engine, Base
from app.routers import blog, user, authentication


Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)