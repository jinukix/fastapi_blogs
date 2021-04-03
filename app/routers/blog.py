from typing import List, Optional

from fastapi import Depends, status
from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.repository import blog
from app.token import get_current_user


router = APIRouter(
    prefix="/blog",
    tags=["Blogs"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
async def all(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
):
    return blog.get_all(db, offset, limit)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    req: schemas.Blog,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return blog.create(req, current_user, db)


@router.delete("/", status_code=status.HTTP_200_OK)
async def destroy(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return blog.destroy(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update(
    id: int,
    req: schemas.Blog,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return blog.put(id, req, db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def show(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return blog.get(id, db)
