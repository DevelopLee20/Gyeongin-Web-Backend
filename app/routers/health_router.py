"""헬스체크 API Router"""

from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from app.base.base_response import BaseResponse
from app.db.mongo_db import mongo_db

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", tags=["Health"])
async def health_check():
    """헬스체크 API"""
    return BaseResponse(
        status_code=HTTP_200_OK, detail="헬스체크 성공", data={"status": "healthy"}
    )


@router.get("/db", tags=["Health"])
async def health_check_db():
    """DB 헬스체크 API"""
    try:
        await mongo_db.command("ping")  # MongoDB에 ping 명령어 전송
        return BaseResponse(
            status_code=HTTP_200_OK,
            detail="DB 헬스체크 성공",
            data={"status": "healthy"},
        )
    except Exception as e:
        return BaseResponse(
            status_code=500, detail="DB 헬스체크 실패", data={"error": str(e)}
        )
