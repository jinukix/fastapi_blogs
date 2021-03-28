from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(40))
    body = Column(String(40))
    user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="blogs")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40))
    email = Column(String(100))
    password = Column(String(300))

    blogs = relationship("Blog", back_populates="creator")
