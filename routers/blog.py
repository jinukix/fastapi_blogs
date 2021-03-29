from typing import List

from fastapi import Depends, status
from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import schemas, database
from repository import blog


get_db = database.get_db

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    return blog.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(req: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(req, db)


@router.delete("/", status_code=status.HTTP_200_OK)
def destroy(id: int, db: Session = Depends(get_db)):
    return blog.destroy(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, req: schemas.Blog, db: Session = Depends(get_db)):
    return blog.put(id, db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    return blog.get(id, db)