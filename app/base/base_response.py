from pydantic import BaseModel, Field
from typing import TypeVar

typeT = TypeVar("T")


class BaseResponse(BaseModel):
    status_code: int = Field(..., description="상태 코드")
    detail: str = Field(..., description="상세 메시지")
    data: typeT = Field(..., description="응답 데이터")
