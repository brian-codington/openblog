# backend/api/routes/media.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from core.auth import get_current_user
from core.storage import upload_to_s3
import uuid

router = APIRouter()

ALLOWED_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
MAX_SIZE_MB = 10


@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    """Upload an image to S3-compatible storage."""
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"File type not allowed: {file.content_type}")

    contents = await file.read()
    if len(contents) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File exceeds {MAX_SIZE_MB}MB limit")

    ext = file.filename.rsplit('.', 1)[-1].lower()
    key = f"media/{uuid.uuid4().hex}.{ext}"

    url = await upload_to_s3(key, contents, file.content_type)
    return {"url": url, "key": key, "filename": file.filename}
