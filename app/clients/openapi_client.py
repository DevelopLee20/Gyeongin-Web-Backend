import httpx
from starlette.status import HTTP_200_OK
from fastapi import HTTPException

from app.responses.openapi_response import OpenAPIResultDTO
from app.core.settings import settings


class OpenAPIClient:
    endpoint = "https://apis.data.go.kr/1230000/ao/PubDataOpnStdService/getDataSetOpnStdScsbidInfo"

    @classmethod
    async def get_data(
        cls, pageNo: str, numOfRows: str, opengBgnDt: str, opengEndDt: str
    ) -> OpenAPIResultDTO | None:
        """오픈API 낙찰 정보 조회

        Args:
            serviceKey (str): 공공데이터포털에서 받은 인증키
            pageNo (str): 페이지번호
            numOfRows (str): 한 페이지 결과 수
            type_ (str): 오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json'으로 지정
            bsnsDivCd (str): 업무 구분코드가 1: 물품, 3: 공사, 5: 용역
            opengBgnDt (str): 개찰일시범위 시작(1주일로 제한)
            opengEndDt (str): 개찰일시범위 종료(1주일로 제한)

        Returns:
            OpenAPIResultDTO | None: _description_
        """
        params = {
            "serviceKey": settings.OPENAPI_API_KEY,
            "pageNo": pageNo,
            "numOfRows": numOfRows,
            "type": "json",
            "bsnsDivCd": "3",
            "opengBgnDt": opengBgnDt,
            "opengEndDt": opengEndDt,
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(cls.endpoint, params=params)

                if response.status_code == HTTP_200_OK:
                    return OpenAPIResultDTO.model_validate(response.json())
                else:
                    # print(f"Error: Received status code {response.status_code}")
                    return None
        except HTTPException:
            return None
