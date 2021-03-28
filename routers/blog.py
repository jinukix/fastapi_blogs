from typing import List

from fastapi import Depends, status
from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import schemas, database, models


router = APIRouter()


@router.get(
    "/blog", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog], tags=["blogs"]
)
def all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs