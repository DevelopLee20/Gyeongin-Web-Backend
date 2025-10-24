from pydantic import BaseModel
from typing import List


class BidItemDTO(BaseModel):
    bidNtceNo: str
    bidNtceOrd: str
    bidNtceNm: str
    bsnsDivNm: str
    cntrctCnclsSttusNm: str
    cntrctCnclsMthdNm: str
    bidwinrDcsnMthdNm: str
    ntceInsttNm: str
    ntceInsttCd: str
    dmndInsttNm: str
    dmndInsttCd: str
    sucsfLwstlmtRt: str | None = None
    presmptPrce: str | None = None
    rsrvtnPrce: str | None = None
    bssAmt: str | None = None
    opengDate: str | None = None
    opengTm: str | None = None
    opengRsltDivNm: str | None = None
    opengRank: str | None = None
    bidprcCorpBizrno: str | None = None
    bidprcCorpNm: str | None = None
    bidprcCorpCeoNm: str | None = None
    bidprcAmt: str | None = None
    bidprcRt: str | None = None
    bidprcDate: str | None = None
    bidprcTm: str | None = None
    sucsfYn: str | None = None
    dqlfctnRsn: str | None = None
    fnlSucsfAmt: str | None = None
    fnlSucsfRt: str | None = None
    fnlSucsfDate: str | None = None
    fnlSucsfCorpNm: str | None = None
    fnlSucsfCorpCeoNm: str | None = None
    fnlSucsfCorpOfclNm: str | None = None
    fnlSucsfCorpBizrno: str | None = None
    fnlSucsfCorpAdrs: str | None = None
    fnlSucsfCorpContactTel: str | None = None
    dataBssDate: str | None = None


class ResponseBodyDTO(BaseModel):
    items: List[BidItemDTO]
    numOfRows: int
    pageNo: int
    totalCount: int


class ResponseHeaderDTO(BaseModel):
    resultCode: str
    resultMsg: str


class OpenAPIResponseDTO(BaseModel):
    header: ResponseHeaderDTO
    body: ResponseBodyDTO


class OpenAPIResultDTO(BaseModel):
    response: OpenAPIResponseDTO
