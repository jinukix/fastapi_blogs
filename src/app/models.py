from sqlalchemy.sql.expression import column
from sqlalchemy.sql.functions import char_length
from .database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(40))
    body = Column(String(40))