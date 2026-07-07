# backend/api/models/author.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from core.database import Base


class Author(Base):
    __tablename__ = 'authors'

    id       = Column(Integer, primary_key=True)
    name     = Column(String(100), nullable=False)
    email    = Column(String(255), unique=True, nullable=False)
    bio      = Column(Text)
    avatar   = Column(String(500))
    password = Column(String(255), nullable=False)

    posts = relationship('Post', back_populates='author')
