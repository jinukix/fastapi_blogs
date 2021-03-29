from fastapi import APIRouter
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session

from app import database, models, schemas
from app.hashing import Hash

get_db = database.get_db

router = APIRouter(
    prefix="/login",
    tags=["Authentication"],
)


@router.post("/")
def login(req: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not Hash.verify(user.password, req.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")

    return user
