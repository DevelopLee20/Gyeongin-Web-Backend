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

    @classmethod
    async def find_all_bids(cls, skip: int = 0, limit: int = 50) -> list[BidDocument]:
        """모든 입찰 문서 조회 (페이지네이션)

        Args:
            skip: 건너뛸 문서 개수
            limit: 조회할 문서 개수

        Returns:
            입찰 문서 리스트
        """
        cursor = cls._collection.find().skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        return [cls._parse(doc) for doc in documents]

    @classmethod
    async def find_bid_by_id(cls, bid_id: str) -> BidDocument | None:
        """ID로 입찰 문서 조회

        Args:
            bid_id: 입찰 문서 ID

        Returns:
            입찰 문서 또는 None
        """
        from bson import ObjectId

        try:
            document = await cls._collection.find_one({"_id": ObjectId(bid_id)})
            return cls._parse(document) if document else None
        except Exception:
            return None

    @classmethod
    async def find_bid_by_announcement_number(
        cls, announcement_number: str
    ) -> BidDocument | None:
        """공고번호로 입찰 문서 조회

        Args:
            announcement_number: 공고번호

        Returns:
            입찰 문서 또는 None
        """
        document = await cls._collection.find_one(
            {"announcement_number": announcement_number}
        )
        return cls._parse(document) if document else None

    @classmethod
    async def update_bid(cls, bid_id: str, bid_document: BidDocument) -> bool:
        """입찰 문서 업데이트

        Args:
            bid_id: 입찰 문서 ID
            bid_document: 업데이트할 입찰 문서

        Returns:
            성공 여부
        """
        from bson import ObjectId

        try:
            # _id 제외한 필드만 업데이트
            update_data = dataclasses.asdict(bid_document)
            update_data.pop("_id", None)

            result = await cls._collection.update_one(
                {"_id": ObjectId(bid_id)}, {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception:
            return False

    @classmethod
    async def delete_bid(cls, bid_id: str) -> bool:
        """입찰 문서 삭제

        Args:
            bid_id: 입찰 문서 ID

        Returns:
            성공 여부
        """
        from bson import ObjectId

        try:
            result = await cls._collection.delete_one({"_id": ObjectId(bid_id)})
            return result.deleted_count > 0
        except Exception:
            return False

    @classmethod
    async def count_all_bids(cls) -> int:
        """전체 입찰 문서 개수 조회

        Returns:
            전체 입찰 문서 개수
        """
        return await cls._collection.count_documents({})
