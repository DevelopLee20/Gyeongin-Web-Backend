from fastapi import FastAPI

from app.routers import health_router

app = FastAPI()

# Include Router
app.include_router(health_router.router)
