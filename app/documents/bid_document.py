import dataclasses
from datetime import datetime
from typing import Optional

from app.base.base_document import BaseDocument


@dataclasses.dataclass(kw_only=True, frozen=True)
class BidDocument(BaseDocument):
    number: Optional[float]  # 번호
    type: str  # 타입
    participation_deadline: Optional[int]  # 참가마감 (일수 또는 코드)
    bid_deadline: datetime  # 투찰마감
    bid_date: datetime  # 입찰일
    ordering_agency: str  # 발주기관
    announcement_name: str  # 공고명
    announcement_number: str  # 공고번호 (중복 체크 기준)
    industry: str  # 업종
    region: str  # 지역
    estimated_price: int  # 추정가격
    base_amount: int  # 기초금액
    first_place_company: str  # 1순위업체
    winning_bid_amount: int  # 낙찰금액
    expected_price: int  # 예정가격
    expected_adjustment: float  # 예정사정
    base_to_winning_ratio: float  # 기초/낙찰 (소수점 5자리)
    expected_to_winning_ratio: float  # 예정/낙찰 (소수점 5자리)
    estimated_to_winning_ratio: float  # 추정/낙찰 (소수점 5자리)
