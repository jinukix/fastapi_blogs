from typing import List
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from . import schemas, models
from .database import engine, Base, get_db
from .hashing import Hash
from routers import blog

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(blog.router)


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create(req: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=req.title, body=req.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete("/blog", status_code=status.HTTP_200_OK, tags=["blogs"])
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )

    blog.delete(synchronize_session=False)
    db.commit()
    return "done"


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update(id: int, req: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )

    blog.update(dict(req))
    db.commit()
    return "updated"


@app.get(
    "/blog", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog], tags=["blogs"]
)
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get(
    "/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=["blogs"]
)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available"
        )

    return blog


@app.post("/user", tags=["users"])
def create_user(req: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=req.name, email=req.email, password=Hash.bcrypt(req.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}", response_model=schemas.ShowUser, tags=["users"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available"
        )

    return user
