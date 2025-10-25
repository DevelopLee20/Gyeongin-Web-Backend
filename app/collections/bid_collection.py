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
    ) -> tuple[int, int, list[str]]:
        """입찰 문서 일괄 삽입/업데이트 (upsert)

        Args:
            bid_documents: 삽입/업데이트할 입찰 문서 리스트

        Returns:
            (삽입된 개수, 업데이트된 개수, 업데이트된 공고번호 리스트)
        """
        if not bid_documents:
            return 0, 0, []

        from pymongo import UpdateOne

        # bulk_write를 위한 operations 생성
        operations = []
        announcement_numbers = []

        for bid_doc in bid_documents:
            doc_dict = dataclasses.asdict(bid_doc)
            # _id 필드 제거 (upsert 시 MongoDB가 자동 생성하거나 기존 것 유지)
            doc_dict.pop("_id", None)

            operations.append(
                UpdateOne(
                    {"announcement_number": bid_doc.announcement_number},
                    {"$set": doc_dict},
                    upsert=True,
                )
            )
            announcement_numbers.append(bid_doc.announcement_number)

        # bulk_write 실행
        if not operations:
            return 0, 0, []

        result = await cls._collection.bulk_write(operations)

        # upserted된 공고번호 수집
        upserted_announcement_numbers = set()
        if result.upserted_ids:
            for upserted_id in result.upserted_ids.values():
                doc = await cls._collection.find_one({"_id": upserted_id})
                if doc:
                    upserted_announcement_numbers.add(doc["announcement_number"])

        # 업데이트된 공고번호 = 전체 - upserted된 것
        # matched_count는 기존에 존재하던 문서 개수 (수정 여부와 무관)
        updated_list = [
            num
            for num in announcement_numbers
            if num not in upserted_announcement_numbers
        ]

        inserted_count = result.upserted_count if result.upserted_count else 0
        # matched_count - upserted_count = 실제로 업데이트 시도한 문서 개수
        updated_count = result.matched_count if result.matched_count else 0

        return inserted_count, updated_count, updated_list

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
