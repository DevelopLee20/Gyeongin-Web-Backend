from fastapi import APIRouter, Query

from app.base.base_response import BaseResponse
from starlette.status import HTTP_200_OK
from app.requests.openapi_request import OpenAPIRequestDTO
from app.services.openapi_service import OpenAPIService

router = APIRouter(prefix="/openapi", tags=["OpenAPI"])


@router.get("/result", tags=["OpenAPI"])
async def get_openapi_result(
    pageNo: str = Query(default="1", description="페이지 번호"),
    numOfRows: str = Query(default="5", description="한 페이지 결과 수"),
    opengBgnDt: str = Query(
        default="202401010000", description="개찰일시범위 시작(YYYYMMDDhhmm)"
    ),
    opengEndDt: str = Query(
        default="202401052359", description="개찰일시범위 종료(YYYYMMDDhhmm)"
    ),
):
    request = OpenAPIRequestDTO(
        pageNo=pageNo, numOfRows=numOfRows, opengBgnDt=opengBgnDt, opengEndDt=opengEndDt
    )
    response = await OpenAPIService.get_successful_response(request)

    return BaseResponse(
        status_code=HTTP_200_OK, detail="오픈API 요청 성공", data=response
    )
