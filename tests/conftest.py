import pytest
from fastapi.testclient import TestClient
import httpx
from httpx import AsyncClient

from app.main import app


# 동기식 테스트 클라이언트
@pytest.fixture(scope="module")
def client():
    """Synchronous test client fixture"""
    return TestClient(app)


# 비동기식 테스트 클라이언트
@pytest.fixture(scope="module")
async def async_client():
    """Asynchronous test client fixture"""
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
