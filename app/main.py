from fastapi import FastAPI

from app.routers import health_router
from app.routers import bid_router

app = FastAPI()

# Include Router
app.include_router(health_router.router)
app.include_router(bid_router.router)
