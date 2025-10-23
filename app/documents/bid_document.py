import dataclasses

from app.base.base_document import BaseDocument


@dataclasses.dataclass(kw_only=True, frozen=True)
class BidDocument(BaseDocument):
    name: str
