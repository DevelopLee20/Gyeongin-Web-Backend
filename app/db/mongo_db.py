from motor.motor_asyncio import AsyncIOMotorClient
from app.core.settings import settings

# MongoDB 클라이언트 설정
client = AsyncIOMotorClient(settings.MONGO_DB_URL)  # type: ignore

# 필요한 MongoDB 컬렉션을 가져옵니다
mongo_db = client["base"]
