from app.db.mongo_db import db
from typing import Any
import dataclasses

from app.documents.bid_document import BidDocument


class BidCollection:
    _collection = db["bid"]

    @classmethod
    async def create_indexes(cls):
        """인덱스 생성 (공고번호 unique index)"""
        await cls._collection.create_index("announcement_number", unique=False)

    @classmethod
    def _parse(cls, document: dict[str, Any]) -> BidDocument:
        return BidDocument(
            _id=document["_id"],
            number=document.get("number"),
            type=document["type"],
            participation_deadline=document["participation_deadline"],
            bid_deadline=document["bid_deadline"],
            bid_date=document["bid_date"],
            ordering_agency=document["ordering_agency"],
            announcement_name=document["announcement_name"],
            announcement_number=document["announcement_number"],
            industry=document["industry"],
            region=document["region"],
            estimated_price=document["estimated_price"],
            base_amount=document["base_amount"],
            first_place_company=document["first_place_company"],
            winning_bid_amount=document["winning_bid_amount"],
            expected_price=document["expected_price"],
            expected_adjustment=document["expected_adjustment"],
            base_to_winning_ratio=document["base_to_winning_ratio"],
            expected_to_winning_ratio=document["expected_to_winning_ratio"],
            estimated_to_winning_ratio=document["estimated_to_winning_ratio"],
        )

    @classmethod
    async def insert_bid(cls, bid_document: BidDocument) -> BidDocument | None:
        """입찰 문서 삽입"""
        result = await cls._collection.insert_one(dataclasses.asdict(bid_document))

        return result.inserted_id if result else None

    @classmethod
    async def check_duplicate_by_announcement_number(
        cls, announcement_number: str
    ) -> bool:
        """공고번호로 중복 체크

        Args:
            announcement_number: 공고번호

        Returns:
            중복이면 True, 아니면 False
        """
        count = await cls._collection.count_documents(
            {"announcement_number": announcement_number}
        )
        return count > 0

    @classmethod
    async def bulk_insert_bids(
        cls, bid_documents: list[BidDocument]
    ) -> tuple[int, list[str]]:
        """입찰 문서 일괄 삽입 (중복 체크 포함)

        Args:
            bid_documents: 삽입할 입찰 문서 리스트

        Returns:
            (저장된 개수, 중복된 공고번호 리스트)
        """
        if not bid_documents:
            return 0, []

        duplicates = []
        to_insert = []

        for bid_doc in bid_documents:
            # 중복 체크
            is_duplicate = await cls.check_duplicate_by_announcement_number(
                bid_doc.announcement_number
            )

            if is_duplicate:
                duplicates.append(bid_doc.announcement_number)
            else:
                to_insert.append(dataclasses.asdict(bid_doc))

        # 삽입할 문서가 있으면 bulk insert
        inserted_count = 0
        if to_insert:
            result = await cls._collection.insert_many(to_insert)
            inserted_count = len(result.inserted_ids) if result else 0

        return inserted_count, duplicates
