from fastapi import Depends, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session

from app import database, models
from app.hashing import Hash
from app.token import create_access_token

get_db = database.get_db

router = APIRouter(
    prefix="/login",
    tags=["Authentication"],
)


@router.post("/")
def login(req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not Hash.verify(user.password, req.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
