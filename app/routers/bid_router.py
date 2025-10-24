"""입찰 데이터 API Router"""

from fastapi import APIRouter, UploadFile, File
from starlette.status import HTTP_200_OK

from app.responses.bid_response import BidUploadResponse
from app.services.bid_service import BidService

router = APIRouter(prefix="/bid", tags=["Bid"])


@router.post("/upload", tags=["Bid"])
async def upload_bid_data(file: UploadFile = File(...)):
    """입찰 데이터 업로드 API

    Args:
        file: 업로드할 엑셀 파일 (.xls 또는 .xlsx)

    Returns:
        저장된 개수, 중복된 데이터 정보
    """
    data = await BidService.upload_bid_data(file)

    return BidUploadResponse(
        status_code=HTTP_200_OK, detail="입찰 데이터 업로드 성공", data=data
    )
