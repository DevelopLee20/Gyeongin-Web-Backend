import pytest
from starlette.status import HTTP_200_OK


class TestHealthCheck:
    @pytest.mark.asyncio
    async def test_health_check_async(self, async_client):
        """비동기 방식 헬스체크 테스트"""
        response = await async_client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status_code"] == HTTP_200_OK
        assert data["detail"] == "헬스체크 성공"
        assert data["data"]["status"] == "healthy"

    # def test_health_check_sync(self, client):
    #     """동기 방식 헬스체크 테스트"""
    #     response = client.get("/health/")

    #     assert response.status_code == 200
    #     data = response.json()

    #     assert data["status_code"] == HTTP_200_OK
    #     assert data["detail"] == "헬스체크 성공"
    #     assert data["data"]["status"] == "healthy"

    # def test_health_check_response_structure(self, client):
    #     """헬스체크 응답 구조 테스트"""
    #     response = client.get("/health/")
    #     data = response.json()

    #     # 응답 구조 검증
    #     assert "status_code" in data
    #     assert "detail" in data
    #     assert "data" in data
    #     assert isinstance(data["data"], dict)
    #     assert "status" in data["data"]

    # @pytest.mark.parametrize("_", range(10))
    # def test_health_check_parallel(self, client, _):
    #     """병렬 헬스체크 테스트 (10개 병렬 실행)"""
    #     response = client.get("/health/")

    #     assert response.status_code == 200
    #     data = response.json()
    #     assert data["status_code"] == HTTP_200_OK
    #     assert data["data"]["status"] == "healthy"
