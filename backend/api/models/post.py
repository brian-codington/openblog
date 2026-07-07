# backend/api/models/post.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
import enum

post_tags = Table(
    'post_tags', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id',  Integer, ForeignKey('tags.id'),  primary_key=True)
)


class PostStatus(str, enum.Enum):
    draft     = 'draft'
    published = 'published'
    archived  = 'archived'


class Post(Base):
    __tablename__ = 'posts'

    id           = Column(Integer, primary_key=True, index=True)
    title        = Column(String(255), nullable=False)
    slug         = Column(String(255), unique=True, index=True, nullable=False)
    content      = Column(Text)
    excerpt      = Column(String(500))
    status       = Column(Enum(PostStatus), default=PostStatus.draft)
    author_id    = Column(Integer, ForeignKey('authors.id'), nullable=False)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True))

    author = relationship('Author', back_populates='posts')
    tags   = relationship('Tag', secondary=post_tags, back_populates='posts')


class Tag(Base):
    __tablename__ = 'tags'

    id    = Column(Integer, primary_key=True)
    name  = Column(String(100), unique=True, nullable=False)
    slug  = Column(String(100), unique=True, nullable=False)
    posts = relationship('Post', secondary=post_tags, back_populates='tags')
