import pandas as pd
from fastapi import UploadFile, HTTPException
from io import BytesIO

from app.responses.bid_response import BidUploadData
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
