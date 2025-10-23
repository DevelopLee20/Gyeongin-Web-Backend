from fastapi import APIRouter

from app.base.base_response import BaseResponse

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/", tags=["Health"])
async def health_check():
    return BaseResponse(status_code=200, detail="헬스체크 성공", data={"status": "healthy"})
