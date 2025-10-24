from pydantic import BaseModel

from app.base.base_response import BaseResponse


class BidUploadData(BaseModel):
    """입찰 데이터 업로드 모델"""

    inserted_count: int  # 저장된 개수
    duplicate_count: int  # 중복된 개수
    duplicates: list[str]  # 중복된 공고번호 리스트


class BidUploadResponse(BaseResponse):
    """입찰 데이터 업로드 응답 모델"""

    data: BidUploadData
