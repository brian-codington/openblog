# backend/api/routes/posts.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from core.database import get_db
from core.auth import get_current_user
from api.models.post import Post, Tag
from api.schemas.post import PostCreate, PostUpdate, PostResponse
from slugify import slugify

router = APIRouter()


@router.get("/", response_model=list[PostResponse])
async def list_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    tag: Optional[str] = None,
    status: str = "published",
    db: AsyncSession = Depends(get_db)
):
    """List posts with pagination and optional tag filter."""
    query = select(Post).where(Post.status == status)

    if tag:
        query = query.join(Post.tags).where(Tag.slug == tag)

    query = query.order_by(Post.published_at.desc()) \
                 .offset((page - 1) * limit) \
                 .limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{slug}", response_model=PostResponse)
async def get_post(slug: str, db: AsyncSession = Depends(get_db)):
    """Get a single post by slug."""
    result = await db.execute(select(Post).where(Post.slug == slug))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/", response_model=PostResponse, status_code=201)
async def create_post(
    post_data: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Create a new post."""
    post = Post(
        title=post_data.title,
        slug=post_data.slug or slugify(post_data.title),
        content=post_data.content,
        excerpt=post_data.excerpt,
        status=post_data.status,
        author_id=current_user.id
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


@router.patch("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Update an existing post."""
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your post")

    for field, value in post_data.model_dump(exclude_unset=True).items():
        setattr(post, field, value)

    await db.commit()
    await db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Delete a post."""
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your post")

    await db.delete(post)
    await db.commit()
