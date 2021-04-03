from typing import Optional, List

from fastapi import Depends, status
from fastapi import APIRouter, Query
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.repository import product


router = APIRouter(
    prefix="/product",
    tags=["Products"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Product])
async def all(
    db: Session = Depends(get_db),
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
    name: str = Query(..., min_length=3, max_length=25),
):
    return product.get_all(db, offset, limit, name)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    req: schemas.Product,
    db: Session = Depends(get_db),
):
    return product.create(req, db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Product)
async def show(
    id: int,
    db: Session = Depends(get_db),
):
    return product.get(id, db)