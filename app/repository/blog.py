from typing import Optional

from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas


def get(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")

    return blog


def get_all(db: Session, offset: Optional[int] = 0, limit: Optional[int] = 10):
    blogs = db.query(models.Blog).all()
    return blogs[offset:limit]


def create(req: schemas.Blog, current_user: schemas.User, db: Session):
    new_blog = models.Blog(title=req.title, body=req.body, user_id=current_user.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def destroy(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return "done"


def put(id: int, req: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")

    blog.update(dict(req))
    db.commit()
    return "updated"
