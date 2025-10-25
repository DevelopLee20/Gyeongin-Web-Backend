from pydantic import BaseModel
from datetime import datetime

from app.base.base_response import BaseResponse


class BidUploadData(BaseModel):
    """입찰 데이터 업로드 모델"""

    inserted_count: int  # 새로 삽입된 개수
    updated_count: int  # 업데이트된 개수
    updated_list: list[str]  # 업데이트된 공고번호 리스트


class BidUploadResponse(BaseResponse):
    """입찰 데이터 업로드 응답 모델"""

    data: BidUploadData


class BidData(BaseModel):
    """입찰 문서 응답 데이터 모델"""

    id: str  # MongoDB ObjectId를 문자열로 변환
    number: float | None
    type: str
    participation_deadline: int | None
    bid_deadline: datetime
    bid_date: datetime
    ordering_agency: str
    announcement_name: str
    announcement_number: str
    industry: str
    region: str
    estimated_price: int
    base_amount: int
    first_place_company: str
    winning_bid_amount: int
    expected_price: int
    expected_adjustment: float
    base_to_winning_ratio: float
    expected_to_winning_ratio: float
    estimated_to_winning_ratio: float


class BidResponse(BaseResponse):
    """입찰 문서 단일 응답 모델"""

    data: BidData


class BidListData(BaseModel):
    """입찰 문서 리스트 응답 데이터 모델"""

    total: int  # 전체 개수
    items: list[BidData]  # 입찰 문서 리스트
    page: int  # 현재 페이지
    size: int  # 페이지 크기


class BidListResponse(BaseResponse):
    """입찰 문서 리스트 응답 모델"""

    data: BidListData
