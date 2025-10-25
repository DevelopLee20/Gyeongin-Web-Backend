import pandas as pd
from fastapi import UploadFile, HTTPException
from io import BytesIO

from app.responses.bid_response import BidUploadData, BidData, BidListData
from app.requests.bid_request import BidCreateRequest, BidUpdateRequest
from app.collections.bid_collection import BidCollection
from app.documents.bid_document import BidDocument
from app.utils.bid_utils import BidUtils


class BidService:
    @classmethod
    async def upload_bid_data(cls, uploaded_file: UploadFile) -> BidUploadData:
        """엑셀 파일 업로드 및 MongoDB 저장

        Args:
            uploaded_file: 업로드된 엑셀 파일

        Returns:
            저장 결과 (저장 개수, 중복 개수, 중복 리스트)
        """
        # 파일 확장자 검증
        if not uploaded_file.filename.endswith((".xls", ".xlsx")):
            raise HTTPException(
                status_code=400, detail="엑셀 파일만 업로드 가능합니다."
            )

        try:
            # 파일 읽기 (날짜 자동 파싱 방지)
            contents = await uploaded_file.read()
            df = pd.read_excel(BytesIO(contents), dtype=str)

            # 데이터 파싱
            bid_documents = []

            for _, row in df.iterrows():
                try:
                    # 공고번호가 없으면 스킵
                    announcement_number = BidUtils.parse_string(row["공고번호"])
                    if not announcement_number:
                        continue

                    bid_doc = BidDocument(
                        number=BidUtils.parse_optional_float(row["번호"]),
                        type=BidUtils.parse_string(row["타입"]),
                        participation_deadline=BidUtils.parse_optional_int(
                            row["참가마감"]
                        ),
                        bid_deadline=BidUtils.parse_datetime(row["투찰마감"]),
                        bid_date=BidUtils.parse_datetime(row["입찰일"]),
                        ordering_agency=BidUtils.parse_string(row["발주기관"]),
                        announcement_name=BidUtils.parse_string(row["공고명"]),
                        announcement_number=announcement_number,
                        industry=BidUtils.parse_string(row["업종"]),
                        region=BidUtils.parse_string(row["지역"]),
                        estimated_price=BidUtils.parse_integer(row["추정가격"]),
                        base_amount=BidUtils.parse_integer(row["기초금액"]),
                        first_place_company=BidUtils.parse_string(row["1순위업체"]),
                        winning_bid_amount=BidUtils.parse_integer(row["낙찰금액"]),
                        expected_price=BidUtils.parse_integer(row["예정가격"]),
                        expected_adjustment=BidUtils.parse_ratio(row["예정사정"]),
                        base_to_winning_ratio=BidUtils.parse_ratio(row["기초/낙찰"]),
                        expected_to_winning_ratio=BidUtils.parse_ratio(
                            row["예정/낙찰"]
                        ),
                        estimated_to_winning_ratio=BidUtils.parse_ratio(
                            row["추정/낙찰"]
                        ),
                    )
                    bid_documents.append(bid_doc)

                except Exception as e:
                    # 개별 row 파싱 실패는 로깅만 하고 계속 진행
                    print(
                        f"Row 파싱 실패 (공고번호: {row.get('공고번호', 'N/A')}): {str(e)}"
                    )
                    continue

            # MongoDB에 bulk insert
            inserted_count, duplicates = await BidCollection.bulk_insert_bids(
                bid_documents
            )

            return BidUploadData(
                inserted_count=inserted_count,
                duplicate_count=len(duplicates),
                duplicates=duplicates,
            )

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"파일 처리 중 오류 발생: {str(e)}"
            )

    @classmethod
    def _document_to_data(cls, document: BidDocument) -> BidData:
        """BidDocument를 BidData로 변환"""
        return BidData(
            id=str(document._id),
            number=document.number,
            type=document.type,
            participation_deadline=document.participation_deadline,
            bid_deadline=document.bid_deadline,
            bid_date=document.bid_date,
            ordering_agency=document.ordering_agency,
            announcement_name=document.announcement_name,
            announcement_number=document.announcement_number,
            industry=document.industry,
            region=document.region,
            estimated_price=document.estimated_price,
            base_amount=document.base_amount,
            first_place_company=document.first_place_company,
            winning_bid_amount=document.winning_bid_amount,
            expected_price=document.expected_price,
            expected_adjustment=document.expected_adjustment,
            base_to_winning_ratio=document.base_to_winning_ratio,
            expected_to_winning_ratio=document.expected_to_winning_ratio,
            estimated_to_winning_ratio=document.estimated_to_winning_ratio,
        )

    @classmethod
    async def get_bids(cls, page: int = 1, size: int = 100) -> BidListData:
        """입찰 문서 목록 조회

        Args:
            page: 페이지 번호 (1부터 시작)
            size: 페이지 크기

        Returns:
            입찰 문서 리스트 데이터
        """
        skip = (page - 1) * size
        documents = await BidCollection.find_all_bids(skip=skip, limit=size)
        total = await BidCollection.count_all_bids()

        return BidListData(
            total=total,
            items=[cls._document_to_data(doc) for doc in documents],
            page=page,
            size=size,
        )

    @classmethod
    async def get_bid_by_id(cls, bid_id: str) -> BidData | None:
        """ID로 입찰 문서 조회

        Args:
            bid_id: 입찰 문서 ID

        Returns:
            입찰 문서 데이터 또는 None
        """
        document = await BidCollection.find_bid_by_id(bid_id)
        if not document:
            return None
        return cls._document_to_data(document)

    @classmethod
    async def get_bid_by_announcement_number(
        cls, announcement_number: str
    ) -> BidData | None:
        """공고번호로 입찰 문서 조회

        Args:
            announcement_number: 공고번호

        Returns:
            입찰 문서 데이터 또는 None
        """
        document = await BidCollection.find_bid_by_announcement_number(
            announcement_number
        )
        if not document:
            return None
        return cls._document_to_data(document)

    @classmethod
    async def create_bid(cls, request: BidCreateRequest) -> str | None:
        """입찰 문서 생성

        Args:
            request: 입찰 문서 생성 요청

        Returns:
            생성된 문서 ID 또는 None
        """
        # 중복 체크
        is_duplicate = await BidCollection.check_duplicate_by_announcement_number(
            request.announcement_number
        )
        if is_duplicate:
            raise HTTPException(
                status_code=400,
                detail=f"이미 존재하는 공고번호입니다: {request.announcement_number}",
            )

        bid_document = BidDocument(
            number=request.number,
            type=request.type,
            participation_deadline=request.participation_deadline,
            bid_deadline=request.bid_deadline,
            bid_date=request.bid_date,
            ordering_agency=request.ordering_agency,
            announcement_name=request.announcement_name,
            announcement_number=request.announcement_number,
            industry=request.industry,
            region=request.region,
            estimated_price=request.estimated_price,
            base_amount=request.base_amount,
            first_place_company=request.first_place_company,
            winning_bid_amount=request.winning_bid_amount,
            expected_price=request.expected_price,
            expected_adjustment=request.expected_adjustment,
            base_to_winning_ratio=request.base_to_winning_ratio,
            expected_to_winning_ratio=request.expected_to_winning_ratio,
            estimated_to_winning_ratio=request.estimated_to_winning_ratio,
        )

        inserted_id = await BidCollection.insert_bid(bid_document)
        return str(inserted_id) if inserted_id else None

    @classmethod
    async def update_bid(cls, bid_id: str, request: BidUpdateRequest) -> bool:
        """입찰 문서 업데이트

        Args:
            bid_id: 입찰 문서 ID
            request: 입찰 문서 업데이트 요청

        Returns:
            성공 여부
        """
        # 기존 문서 조회
        existing_doc = await BidCollection.find_bid_by_id(bid_id)
        if not existing_doc:
            raise HTTPException(status_code=404, detail="입찰 문서를 찾을 수 없습니다")

        # 업데이트할 필드만 적용
        update_data = request.model_dump(exclude_unset=True)

        # 기존 문서 데이터를 dict로 변환
        import dataclasses

        doc_dict = dataclasses.asdict(existing_doc)

        # 업데이트할 필드 적용
        doc_dict.update(update_data)

        # BidDocument로 재생성
        updated_document = BidDocument(**doc_dict)

        return await BidCollection.update_bid(bid_id, updated_document)

    @classmethod
    async def delete_bid(cls, bid_id: str) -> bool:
        """입찰 문서 삭제

        Args:
            bid_id: 입찰 문서 ID

        Returns:
            성공 여부
        """
        # 문서 존재 확인
        existing_doc = await BidCollection.find_bid_by_id(bid_id)
        if not existing_doc:
            raise HTTPException(status_code=404, detail="입찰 문서를 찾을 수 없습니다")

        return await BidCollection.delete_bid(bid_id)
