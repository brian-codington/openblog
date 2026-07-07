# backend/api/schemas/post.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from api.models.post import PostStatus


class PostBase(BaseModel):
    title:   str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = None
    excerpt: Optional[str] = Field(None, max_length=500)
    status:  PostStatus = PostStatus.draft


class PostCreate(PostBase):
    slug: Optional[str] = None


class PostUpdate(BaseModel):
    title:   Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    excerpt: Optional[str] = None
    status:  Optional[PostStatus] = None
    slug:    Optional[str] = None


class PostResponse(PostBase):
    id:           int
    slug:         str
    author_id:    int
    created_at:   datetime
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True
