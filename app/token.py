from jose import jwt, JWTError
from datetime import datetime, timedelta

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException

from app import models, schemas
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if not user_id:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=user_id)
        return token_data
    except JWTError:
        raise credentials_exception


def create_access_token(user: models.User):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"user_id": user.id}
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return access_token