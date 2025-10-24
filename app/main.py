from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import health_router
from app.routers import bid_router
from app.routers import openapi_router
from app.collections.bid_collection import BidCollection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: 인덱스 생성
    await BidCollection.create_indexes()
    yield
    # Shutdown: 필요한 정리 작업


app = FastAPI(lifespan=lifespan)

# Include Router
app.include_router(health_router.router)
app.include_router(bid_router.router)
app.include_router(openapi_router.router)
