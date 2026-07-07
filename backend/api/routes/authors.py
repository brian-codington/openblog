# backend/api/routes/authors.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import get_db
from api.models.author import Author

router = APIRouter()

@router.get("/{author_id}")
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Author).where(Author.id == author_id))
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author
