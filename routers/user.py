from fastapi import Depends, status, HTTPException
from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.hashing import Hash
from app import schemas, models, database


get_db = database.get_db

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.post("/")
def create_user(req: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=req.name, email=req.email, password=Hash.bcrypt(req.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available"
        )

    return user