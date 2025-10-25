import pytest
import time
from datetime import datetime
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)


class TestBidCRUD:
    """입찰 CRUD API 테스트"""

    def _generate_unique_announcement_number(self):
        """고유한 공고번호 생성"""
        return f"TEST-{int(time.time() * 1000000)}"

    # 테스트용 입찰 데이터
    @pytest.fixture
    def sample_bid_data(self):
        """테스트용 입찰 데이터 fixture"""
        return {
            "number": 1.0,
            "type": "공사",
            "participation_deadline": 5,
            "bid_deadline": "2025-01-20T10:00:00",
            "bid_date": "2025-01-21T14:00:00",
            "ordering_agency": "경인테스트청",
            "announcement_name": "테스트 공사 입찰",
            "announcement_number": "TEST-2025-001",
            "industry": "건설업",
            "region": "서울",
            "estimated_price": 100000000,
            "base_amount": 95000000,
            "first_place_company": "테스트건설",
            "winning_bid_amount": 94000000,
            "expected_price": 96000000,
            "expected_adjustment": 0.98,
            "base_to_winning_ratio": 0.989,
            "expected_to_winning_ratio": 0.979,
            "estimated_to_winning_ratio": 0.94,
        }

    @pytest.fixture
    def update_bid_data(self):
        """테스트용 업데이트 데이터 fixture"""
        return {
            "announcement_name": "수정된 공사 입찰",
            "first_place_company": "수정건설",
            "winning_bid_amount": 93000000,
        }

    @pytest.mark.asyncio
    async def test_create_bid(self, async_client, sample_bid_data):
        """입찰 생성 API 테스트"""
        # 고유한 공고번호 생성
        sample_bid_data["announcement_number"] = self._generate_unique_announcement_number()

        response = await async_client.post("/bid/", json=sample_bid_data)

        assert response.status_code == HTTP_200_OK
        data = response.json()

        assert data["status_code"] == HTTP_201_CREATED
        assert data["detail"] == "입찰 생성 성공"
        assert "id" in data["data"]
        assert isinstance(data["data"]["id"], str)

        # 생성된 ID 반환 (cleanup용)
        return data["data"]["id"]

    @pytest.mark.asyncio
    async def test_create_bid_duplicate(self, async_client, sample_bid_data):
        """중복 공고번호로 입찰 생성 시 실패 테스트"""
        # 고유한 공고번호 생성
        sample_bid_data["announcement_number"] = self._generate_unique_announcement_number()

        # 첫 번째 생성
        await async_client.post("/bid/", json=sample_bid_data)

        # 동일한 공고번호로 재시도
        response = await async_client.post("/bid/", json=sample_bid_data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        data = response.json()
        assert "이미 존재하는 공고번호입니다" in data["detail"]

    @pytest.mark.asyncio
    async def test_get_bids_list(self, async_client, sample_bid_data):
        """입찰 목록 조회 API 테스트"""
        # 테스트 데이터 생성
        sample_bid_data["announcement_number"] = self._generate_unique_announcement_number()
        await async_client.post("/bid/", json=sample_bid_data)

        # 목록 조회
        response = await async_client.get("/bid/?page=1&size=10")

        assert response.status_code == HTTP_200_OK
        data = response.json()

        assert data["status_code"] == HTTP_200_OK
        assert data["detail"] == "입찰 목록 조회 성공"
        assert "total" in data["data"]
        assert "items" in data["data"]
        assert "page" in data["data"]
        assert "size" in data["data"]
        assert isinstance(data["data"]["items"], list)
        assert data["data"]["page"] == 1
        assert data["data"]["size"] == 10

    @pytest.mark.asyncio
    async def test_get_bids_list_pagination(self, async_client):
        """입찰 목록 페이지네이션 테스트"""
        # 첫 번째 페이지 조회
        response_page1 = await async_client.get("/bid/?page=1&size=5")
        data_page1 = response_page1.json()

        assert data_page1["data"]["page"] == 1
        assert data_page1["data"]["size"] == 5

        # 두 번째 페이지 조회
        response_page2 = await async_client.get("/bid/?page=2&size=5")
        data_page2 = response_page2.json()

        assert data_page2["data"]["page"] == 2
        assert data_page2["data"]["size"] == 5

    @pytest.mark.asyncio
    async def test_get_bid_by_id(self, async_client, sample_bid_data):
        """ID로 입찰 조회 API 테스트"""
        # 테스트 데이터 생성
        sample_bid_data["announcement_number"] = self._generate_unique_announcement_number()
        create_response = await async_client.post("/bid/", json=sample_bid_data)
        created_id = create_response.json()["data"]["id"]

        # ID로 조회
        response = await async_client.get(f"/bid/id/{created_id}")

        assert response.status_code == HTTP_200_OK
        data = response.json()

        assert data["status_code"] == HTTP_200_OK
        assert data["detail"] == "입찰 조회 성공"
        assert data["data"]["id"] == created_id
        assert data["data"]["announcement_number"] == sample_bid_data["announcement_number"]
        assert data["data"]["announcement_name"] == sample_bid_data["announcement_name"]

    @pytest.mark.asyncio
    async def test_get_bid_by_id_not_found(self, async_client):
        """존재하지 않는 ID로 입찰 조회 시 404 테스트"""
        # 존재하지 않는 ID (유효한 ObjectId 형식)
        fake_id = "507f1f77bcf86cd799439011"

        response = await async_client.get(f"/bid/id/{fake_id}")

        assert response.status_code == HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "입찰 문서를 찾을 수 없습니다"

    @pytest.mark.asyncio
    async def test_get_bid_by_announcement_number(self, async_client, sample_bid_data):
        """공고번호로 입찰 조회 API 테스트"""
        # 테스트 데이터 생성
        sample_bid_data["announcement_number"] = self._generate_unique_announcement_number()
        await async_client.post("/bid/", json=sample_bid_data)

        # 공고번호로 조회
        announcement_number = sample_bid_data["announcement_number"]
        response = await async_client.get(f"/bid/announcement/{announcement_number}")

        assert response.status_code == HTTP_200_OK
        data = response.json()

        assert data["status_code"] == HTTP_200_OK
        assert data["detail"] == "입찰 조회 성공"
        assert data["data"]["announcement_number"] == announcement_number
        assert data["data"]["announcement_name"] == sample_bid_data["announcement_name"]

    @pytest.mark.asyncio
    async def test_get_bid_by_announcement_number_not_found(self, async_client):
        """존재하지 않는 공고번호로 조회 시 404 테스트"""
        response = await async_client.get("/bid/announcement/NONEXISTENT-999")

        assert response.status_code == HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "입찰 문서를 찾을 수 없습니다"

    @pytest.mark.asyncio
    async def test_update_bid(self, async_client, sample_bid_data, update_bid_data):
        """입찰 업데이트 API 테스트"""
        # 테스트 데이터 생성
        sample_bid_data["announcement_number"] = self._generate_unique_announcement_number()
        create_response = await async_client.post("/bid/", json=sample_bid_data)
        created_id = create_response.json()["data"]["id"]

        # 업데이트 실행
        response = await async_client.put(f"/bid/{created_id}", json=update_bid_data)

        assert response.status_code == HTTP_200_OK
        data = response.json()

        assert data["status_code"] == HTTP_200_OK
        assert data["detail"] == "입찰 업데이트 성공"
        assert data["data"]["success"] is True

        # 업데이트 확인
        get_response = await async_client.get(f"/bid/id/{created_id}")
        updated_data = get_response.json()["data"]

        assert updated_data["announcement_name"] == update_bid_data["announcement_name"]
        assert updated_data["first_place_company"] == update_bid_data["first_place_company"]
        assert updated_data["winning_bid_amount"] == update_bid_data["winning_bid_amount"]
        # 수정하지 않은 필드는 유지되어야 함
        assert updated_data["announcement_number"] == sample_bid_data["announcement_number"]

    @pytest.mark.asyncio
    async def test_update_bid_not_found(self, async_client, update_bid_data):
        """존재하지 않는 입찰 업데이트 시 404 테스트"""
        fake_id = "507f1f77bcf86cd799439011"

        response = await async_client.put(f"/bid/{fake_id}", json=update_bid_data)

        assert response.status_code == HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "입찰 문서를 찾을 수 없습니다"

    @pytest.mark.asyncio
    async def test_delete_bid(self, async_client, sample_bid_data):
        """입찰 삭제 API 테스트"""
        # 테스트 데이터 생성
        sample_bid_data["announcement_number"] = self._generate_unique_announcement_number()
        create_response = await async_client.post("/bid/", json=sample_bid_data)
        created_id = create_response.json()["data"]["id"]

        # 삭제 실행
        response = await async_client.delete(f"/bid/{created_id}")

        assert response.status_code == HTTP_200_OK
        data = response.json()

        assert data["status_code"] == HTTP_200_OK
        assert data["detail"] == "입찰 삭제 성공"
        assert data["data"]["success"] is True

        # 삭제 확인 (조회 시 404)
        get_response = await async_client.get(f"/bid/id/{created_id}")
        assert get_response.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_delete_bid_not_found(self, async_client):
        """존재하지 않는 입찰 삭제 시 404 테스트"""
        fake_id = "507f1f77bcf86cd799439011"

        response = await async_client.delete(f"/bid/{fake_id}")

        assert response.status_code == HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "입찰 문서를 찾을 수 없습니다"

    @pytest.mark.asyncio
    async def test_bid_response_structure(self, async_client, sample_bid_data):
        """입찰 응답 구조 검증 테스트"""
        # 테스트 데이터 생성
        sample_bid_data["announcement_number"] = self._generate_unique_announcement_number()
        create_response = await async_client.post("/bid/", json=sample_bid_data)
        created_id = create_response.json()["data"]["id"]

        # 조회
        response = await async_client.get(f"/bid/id/{created_id}")
        data = response.json()

        # 응답 구조 검증
        assert "status_code" in data
        assert "detail" in data
        assert "data" in data
        assert isinstance(data["data"], dict)

        # 데이터 필드 검증
        bid_data = data["data"]
        expected_fields = [
            "id", "number", "type", "participation_deadline",
            "bid_deadline", "bid_date", "ordering_agency",
            "announcement_name", "announcement_number", "industry",
            "region", "estimated_price", "base_amount",
            "first_place_company", "winning_bid_amount", "expected_price",
            "expected_adjustment", "base_to_winning_ratio",
            "expected_to_winning_ratio", "estimated_to_winning_ratio"
        ]

        for field in expected_fields:
            assert field in bid_data

    @pytest.mark.asyncio
    async def test_partial_update_bid(self, async_client, sample_bid_data):
        """부분 업데이트 테스트 (일부 필드만 수정)"""
        # 테스트 데이터 생성
        sample_bid_data["announcement_number"] = self._generate_unique_announcement_number()
        create_response = await async_client.post("/bid/", json=sample_bid_data)
        created_id = create_response.json()["data"]["id"]

        # 하나의 필드만 업데이트
        partial_update = {"announcement_name": "부분 수정된 공고명"}
        response = await async_client.put(f"/bid/{created_id}", json=partial_update)

        assert response.status_code == HTTP_200_OK

        # 업데이트 확인
        get_response = await async_client.get(f"/bid/id/{created_id}")
        updated_data = get_response.json()["data"]

        # 수정된 필드 확인
        assert updated_data["announcement_name"] == "부분 수정된 공고명"
        # 다른 필드는 원본 유지
        assert updated_data["announcement_number"] == sample_bid_data["announcement_number"]
        assert updated_data["ordering_agency"] == sample_bid_data["ordering_agency"]
