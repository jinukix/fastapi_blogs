from typing import Optional

from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas


def get_all(
    db: Session,
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
    name: Optional[str] = None,
):
    if name:
        products = db.query(models.Product).filter(models.Product.name.ilike(f"%{name}%"))
    else:
        products = db.query(models.Product).all()
    return products[offset:limit]


def create(req: schemas.Product, db: Session):
    new_product = models.Product(name=req.name, price=req.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get(id: int, db: Session):
    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with the id {id} is not available")

    return product
