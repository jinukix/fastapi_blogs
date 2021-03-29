from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Enum,
    Boolean,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.utc_timestamp())
    updated_at = Column(DateTime, default=func.utc_timestamp(), onupdate=func.utc_timestamp())


class Blog(Base, BaseMixin):
    __tablename__ = "blogs"

    title = Column(String(40))
    body = Column(String(40))
    user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="blogs")


class User(Base, BaseMixin):
    __tablename__ = "users"

    email = Column(String(100), unique=True)
    password = Column(String(300))
    name = Column(String(40), nullable=True)
    gender = Column(Enum("Male", "FeMale"))
    sns_type = Column(Enum("Email", "Kakao", "Google"), nullable=True)
    marketing_agree = Column(Boolean, nullable=True, default=True)

    blogs = relationship("Blog", back_populates="creator")
