from app.db.mongo_db import db
from typing import Any
import dataclasses

from app.documents.bid_document import BidDocument


class BidCollection:
    _collection = db["bid"]

    @classmethod
    def _parse(cls, document: dict[str, Any]) -> BidDocument:
        return BidDocument(
            _id=document["_id"],
            name=document["name"],
        )

    @classmethod
    async def insert_bid(cls, bid_document: BidDocument) -> BidDocument | None:
        """입찰 문서 삽입"""
        result = await cls._collection.insert_one(dataclasses.asdict(bid_document))

        return result.inserted_id if result else None
