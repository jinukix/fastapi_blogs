from fastapi import FastAPI

from app.database import engine, Base
from app.routes.api import router


Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router)