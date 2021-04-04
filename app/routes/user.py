import bcrypt

from fastapi import Depends, status, HTTPException
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import get_db
from app.token import create_access_token


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(req: schemas.User, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(req.password.encode("utf-8"), bcrypt.gensalt()).decode()
    new_user = models.User(name=req.name, email=req.email, gender=req.gender, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")

    return user


@router.post("/login", status_code=status.HTTP_200_OK)
def login(req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not bcrypt.checkpw(req.password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")

    access_token = create_access_token(user)

    return {"access_token": access_token, "token_type": "bearer"}