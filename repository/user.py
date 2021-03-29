from fastapi import status, HTTPException
from sqlalchemy.orm.session import Session

from app import models, schemas
from app.hashing import Hash


def create(req: schemas.User, db: Session):
    new_user = models.User(name=req.name, email=req.email, password=Hash.bcrypt(req.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available"
        )

    return user
