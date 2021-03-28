from typing import List

from fastapi import Depends, status, HTTPException
from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import schemas, models, database


get_db = database.get_db

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(req: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=req.title, body=req.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete("/", status_code=status.HTTP_200_OK)
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )

    blog.delete(synchronize_session=False)
    db.commit()
    return "done"


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, req: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )

    blog.update(dict(req))
    db.commit()
    return "updated"


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available"
        )

    return blog