"""헬스체크 API Router"""

from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from app.responses.bid_response import BidUploadResponse
from app.services.bid_service import BidService

router = APIRouter(prefix="/bid", tags=["Bid"])


@router.get("/upload", tags=["Bid"])
async def upload_bid_data():
    """입찰 데이터 업로드 API"""
    data = await BidService.upload_bid_data()

    return BidUploadResponse(
        status_code=HTTP_200_OK, detail="입찰 데이터 업로드 성공", insert_result=data
    )
