from pydantic import BaseModel, Field
from datetime import datetime


class BidCreateRequest(BaseModel):
    """입찰 문서 생성 요청 모델"""

    number: float | None = Field(None, description="번호")
    type: str = Field(..., description="타입")
    participation_deadline: int | None = Field(
        None, description="참가마감 (일수 또는 코드)"
    )
    bid_deadline: datetime = Field(..., description="투찰마감")
    bid_date: datetime = Field(..., description="입찰일")
    ordering_agency: str = Field(..., description="발주기관")
    announcement_name: str = Field(..., description="공고명")
    announcement_number: str = Field(..., description="공고번호")
    industry: str = Field(..., description="업종")
    region: str = Field(..., description="지역")
    estimated_price: int = Field(..., description="추정가격")
    base_amount: int = Field(..., description="기초금액")
    first_place_company: str = Field(..., description="1순위업체")
    winning_bid_amount: int = Field(..., description="낙찰금액")
    expected_price: int = Field(..., description="예정가격")
    expected_adjustment: float = Field(..., description="예정사정")
    base_to_winning_ratio: float = Field(..., description="기초/낙찰")
    expected_to_winning_ratio: float = Field(..., description="예정/낙찰")
    estimated_to_winning_ratio: float = Field(..., description="추정/낙찰")


class BidUpdateRequest(BaseModel):
    """입찰 문서 업데이트 요청 모델"""

    number: float | None = Field(None, description="번호")
    type: str | None = Field(None, description="타입")
    participation_deadline: int | None = Field(
        None, description="참가마감 (일수 또는 코드)"
    )
    bid_deadline: datetime | None = Field(None, description="투찰마감")
    bid_date: datetime | None = Field(None, description="입찰일")
    ordering_agency: str | None = Field(None, description="발주기관")
    announcement_name: str | None = Field(None, description="공고명")
    announcement_number: str | None = Field(None, description="공고번호")
    industry: str | None = Field(None, description="업종")
    region: str | None = Field(None, description="지역")
    estimated_price: int | None = Field(None, description="추정가격")
    base_amount: int | None = Field(None, description="기초금액")
    first_place_company: str | None = Field(None, description="1순위업체")
    winning_bid_amount: int | None = Field(None, description="낙찰금액")
    expected_price: int | None = Field(None, description="예정가격")
    expected_adjustment: float | None = Field(None, description="예정사정")
    base_to_winning_ratio: float | None = Field(None, description="기초/낙찰")
    expected_to_winning_ratio: float | None = Field(None, description="예정/낙찰")
    estimated_to_winning_ratio: float | None = Field(None, description="추정/낙찰")
