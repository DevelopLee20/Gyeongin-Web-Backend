from pydantic import BaseModel
from pydantic import Field


class OpenAPIRequestDTO(BaseModel):
    pageNo: str = Field(default="1", description="페이지 번호")
    numOfRows: str = Field(default="5", description="한 페이지 결과 수")
    opengBgnDt: str = Field(
        "202501010000", description="개찰일시범위 시작(YYYYMMDDhhmm)"
    )
    opengEndDt: str = Field(
        "202501052359", description="개찰일시범위 종료(YYYYMMDDhhmm)"
    )
