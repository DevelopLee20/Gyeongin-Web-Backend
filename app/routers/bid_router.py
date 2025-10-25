"""입찰 데이터 API Router"""

from fastapi import APIRouter, UploadFile, File, Query, Path, HTTPException
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)

from app.responses.bid_response import (
    BidUploadResponse,
    BidResponse,
    BidListResponse,
)
from app.requests.bid_request import BidCreateRequest, BidUpdateRequest
from app.services.bid_service import BidService
from app.base.base_response import BaseResponse

router = APIRouter(prefix="/bid", tags=["Bid"])


@router.post("/upload", tags=["Bid"])
async def upload_bid_data(file: UploadFile = File(...)):
    """입찰 데이터 업로드 API

    Args:
        file: 업로드할 엑셀 파일 (.xls 또는 .xlsx)

    Returns:
        저장된 개수, 중복된 데이터 정보
    """
    data = await BidService.upload_bid_data(file)

    return BidUploadResponse(
        status_code=HTTP_200_OK, detail="입찰 데이터 업로드 성공", data=data
    )


@router.get("", tags=["Bid"], response_model=BidListResponse)
async def get_bids(
    page: int = Query(default=1, ge=1, description="페이지 번호 (1부터 시작)"),
    size: int = Query(default=100, ge=1, le=1000, description="페이지 크기"),
):
    """입찰 문서 목록 조회 API

    Args:
        page: 페이지 번호
        size: 페이지 크기

    Returns:
        입찰 문서 목록
    """
    data = await BidService.get_bids(page=page, size=size)

    return BidListResponse(
        status_code=HTTP_200_OK, detail="입찰 목록 조회 성공", data=data
    )


@router.get("/id/{bid_id}", tags=["Bid"], response_model=BidResponse)
async def get_bid_by_id(bid_id: str = Path(..., description="입찰 문서 ID")):
    """ID로 입찰 문서 조회 API

    Args:
        bid_id: 입찰 문서 ID

    Returns:
        입찰 문서 데이터
    """
    data = await BidService.get_bid_by_id(bid_id)

    if not data:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="입찰 문서를 찾을 수 없습니다"
        )

    return BidResponse(status_code=HTTP_200_OK, detail="입찰 조회 성공", data=data)


@router.get(
    "/announcement/{announcement_number}", tags=["Bid"], response_model=BidResponse
)
async def get_bid_by_announcement_number(
    announcement_number: str = Path(..., description="공고번호"),
):
    """공고번호로 입찰 문서 조회 API

    Args:
        announcement_number: 공고번호

    Returns:
        입찰 문서 데이터
    """
    data = await BidService.get_bid_by_announcement_number(announcement_number)

    if not data:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="입찰 문서를 찾을 수 없습니다"
        )

    return BidResponse(status_code=HTTP_200_OK, detail="입찰 조회 성공", data=data)


@router.post("", tags=["Bid"], response_model=BaseResponse)
async def create_bid(request: BidCreateRequest):
    """입찰 문서 생성 API

    Args:
        request: 입찰 문서 생성 요청

    Returns:
        생성된 입찰 문서 ID
    """
    inserted_id = await BidService.create_bid(request)

    if not inserted_id:
        raise HTTPException(status_code=500, detail="입찰 문서 생성 실패")

    return BaseResponse(
        status_code=HTTP_201_CREATED,
        detail="입찰 생성 성공",
        data={"id": inserted_id},
    )


@router.put("/{bid_id}", tags=["Bid"], response_model=BaseResponse)
async def update_bid(
    bid_id: str = Path(..., description="입찰 문서 ID"),
    request: BidUpdateRequest = ...,
):
    """입찰 문서 업데이트 API

    Args:
        bid_id: 입찰 문서 ID
        request: 입찰 문서 업데이트 요청

    Returns:
        업데이트 결과
    """
    success = await BidService.update_bid(bid_id, request)

    if not success:
        raise HTTPException(status_code=500, detail="입찰 문서 업데이트 실패")

    return BaseResponse(
        status_code=HTTP_200_OK, detail="입찰 업데이트 성공", data={"success": True}
    )


@router.delete("/{bid_id}", tags=["Bid"], response_model=BaseResponse)
async def delete_bid(bid_id: str = Path(..., description="입찰 문서 ID")):
    """입찰 문서 삭제 API

    Args:
        bid_id: 입찰 문서 ID

    Returns:
        삭제 결과
    """
    success = await BidService.delete_bid(bid_id)

    if not success:
        raise HTTPException(status_code=500, detail="입찰 문서 삭제 실패")

    return BaseResponse(
        status_code=HTTP_200_OK, detail="입찰 삭제 성공", data={"success": True}
    )
