from pydantic import BaseModel

from app.base.base_response import BaseResponse


class BidUploadData(BaseModel):
    """입찰 데이터 업로드 모델"""

    count: int


class BidUploadResponse(BaseResponse):
    """입찰 데이터 업로드 응답 모델"""

    insert_result: BidUploadData
