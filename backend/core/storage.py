# backend/core/storage.py
import boto3
from core.config import settings

s3 = boto3.client(
    's3',
    region_name=settings.S3_REGION,
    endpoint_url=settings.S3_ENDPOINT_URL or None
)


async def upload_to_s3(key: str, data: bytes, content_type: str) -> str:
    """Upload a file to S3 and return the public URL."""
    s3.put_object(
        Bucket=settings.S3_BUCKET,
        Key=key,
        Body=data,
        ContentType=content_type,
        ACL='public-read'
    )
    base = settings.S3_ENDPOINT_URL or f"https://{settings.S3_BUCKET}.s3.{settings.S3_REGION}.amazonaws.com"
    return f"{base}/{key}"
