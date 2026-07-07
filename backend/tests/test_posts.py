# backend/tests/test_posts.py
import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_list_posts_returns_200():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_post_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/posts/non-existent-slug")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_post_requires_auth():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/posts", json={
            "title": "Test Post",
            "content": "Hello world",
            "status": "draft"
        })
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
