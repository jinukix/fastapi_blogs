from typing import Optional, List

from fastapi import Depends, status, HTTPException
from fastapi import APIRouter, Query
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import get_db


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Product])
def all(
    db: Session = Depends(get_db),
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
    name: str = Query(None, min_length=3, max_length=25),
):
    if name:
        products = db.query(models.Product).filter(models.Product.name.ilike(f"%{name}%"))
    else:
        products = db.query(models.Product).all()
    return products[offset:limit]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
    req: schemas.Product,
    db: Session = Depends(get_db),
):
    new_product = models.Product(name=req.name, price=req.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Product)
def show(
    id: int,
    db: Session = Depends(get_db),
):
    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with the id {id} is not available")

    return product