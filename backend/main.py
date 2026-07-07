# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.routes import posts, tags, authors, media
from core.config import settings
from core.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="OpenBlog API",
    description="Headless CMS and blogging platform API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(posts.router,   prefix="/api/posts",   tags=["posts"])
app.include_router(tags.router,    prefix="/api/tags",    tags=["tags"])
app.include_router(authors.router, prefix="/api/authors", tags=["authors"])
app.include_router(media.router,   prefix="/api/media",   tags=["media"])


@app.get("/health")
def health():
    return {"status": "ok"}
