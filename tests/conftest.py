import pytest
import pytest_asyncio
import asyncio
from fastapi.testclient import TestClient
import httpx
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.main import app
from app.core.settings import settings


# Event loop fixture - 각 테스트마다 새로운 이벤트 루프 생성
@pytest_asyncio.fixture(scope="function")
def event_loop():
    """Create new event loop for each test"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


# MongoDB 클라이언트 재초기화 fixture
@pytest_asyncio.fixture(scope="function", autouse=True)
async def reset_mongodb_client():
    """Reset MongoDB client for each test to avoid event loop issues"""
    from app.db import mongo_db
    from app.collections import bid_collection

    # 새 클라이언트 생성
    mongo_db.client = AsyncIOMotorClient(settings.MONGO_DB_URL)  # type: ignore
    mongo_db.db = mongo_db.client["base"]

    # Collection 재설정
    bid_collection.BidCollection._collection = mongo_db.db["bids"]

    yield

    # 테스트 후 정리
    mongo_db.client.close()


# 동기식 테스트 클라이언트
@pytest.fixture(scope="module")
def client():
    """Synchronous test client fixture"""
    return TestClient(app)


# 비동기식 테스트 클라이언트
@pytest_asyncio.fixture(scope="function")
async def async_client():
    """Asynchronous test client fixture"""
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
