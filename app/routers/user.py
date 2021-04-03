from fastapi import Depends, status
from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database import get_db
from app.repository import user
from app import schemas

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(req: schemas.User, db: Session = Depends(get_db)):

    """
    `회원가입 API`\n

    Body : name, email, password
    """

    return user.create(req, db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
async def get_user(id: int, db: Session = Depends(get_db)):

    """
    `유저 검색 API`\n

    QS : user_id
    """

    return user.get(id, db)
