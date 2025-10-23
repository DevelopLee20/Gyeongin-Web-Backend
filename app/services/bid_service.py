from fastapi import UploadFile

from app.responses.bid_response import BidUploadData
from app.collections.bid_collection import BidCollection


class BidService:
    @classmethod
    async def upload_bid_data(cls, uploaded_file: UploadFile) -> BidUploadData:
        # 입찰 데이터 업로드 로직 구현
        # File 파싱 코드 작성
        insert_data_list = []
        count = 0
        async for line in insert_data_list:
            result = await BidCollection.insert_bid(line)
            count += result is not None

        return BidUploadData(count=count)
