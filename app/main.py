from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path

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

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# Include Router
app.include_router(health_router.router)
app.include_router(bid_router.router)
app.include_router(openapi_router.router)

# Static files mount
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# Root endpoint to serve index.html
@app.get("/")
async def read_root():
    """루트 경로에서 차트 페이지 제공"""
    return FileResponse(str(static_dir / "index.html"))
