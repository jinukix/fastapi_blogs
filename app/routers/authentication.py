import bcrypt

from fastapi import Depends, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session

from app import models
from app.database import get_db
from app.token import create_access_token


router = APIRouter(
    prefix="/login",
    tags=["Authentication"],
)


@router.post("/", status_code=status.HTTP_200_OK)
def login(req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not bcrypt.checkpw(req.password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")

    access_token = create_access_token(user)

    return {"access_token": access_token, "token_type": "bearer"}
