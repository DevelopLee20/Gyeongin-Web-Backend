from app.clients.openapi_client import OpenAPIClient

from app.requests.openapi_request import OpenAPIRequestDTO
from app.base.base_response import BaseResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


class OpenAPIService:
    @classmethod
    async def get_successful_response(cls, request: OpenAPIRequestDTO):
        response = await OpenAPIClient.get_data(
            pageNo=request.pageNo,
            numOfRows=request.numOfRows,
            opengBgnDt=request.opengBgnDt,
            opengEndDt=request.opengEndDt,
        )

        # 개찰 결과를 불러오지 못했을 때
        if response is None:
            return BaseResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="오픈API 요청 실패",
                data=response,
            )

        return response
