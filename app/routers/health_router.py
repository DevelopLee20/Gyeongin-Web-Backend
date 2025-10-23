"""헬스체크 API Router"""

from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from app.base.base_response import BaseResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", tags=["Health"])
async def health_check():
    """헬스체크 API"""
    return BaseResponse(
        status_code=HTTP_200_OK, detail="헬스체크 성공", data={"status": "healthy"}
    )
