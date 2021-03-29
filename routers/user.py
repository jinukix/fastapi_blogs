from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import schemas, database

from repository import user

get_db = database.get_db

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.post("/")
def create_user(req: schemas.User, db: Session = Depends(get_db)):
    return user.create(req, db)


@router.get("/{id}", response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.create(id, db)
