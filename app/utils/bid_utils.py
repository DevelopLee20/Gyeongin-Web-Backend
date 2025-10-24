"""입찰 데이터 파싱 유틸리티"""

from datetime import datetime
from typing import Any

import pandas as pd


class BidUtils:
    """입찰 데이터 파싱을 위한 유틸리티 클래스"""

    @staticmethod
    def parse_datetime(date_str: str) -> datetime:
        """날짜 문자열을 datetime으로 변환

        형식: "22-03-11 10:00" 또는 "2024.1.18  10:00:00 AM"
        """
        if pd.isna(date_str):
            raise ValueError("Invalid date string: NaN value")

        date_str = str(date_str).strip()

        # 빈 문자열, 'nan', '-', 또는 짧은 숫자만 있는 경우
        if not date_str or date_str.lower() == "nan" or date_str == "-":
            raise ValueError(f"Invalid date string: '{date_str}'")

        # 숫자만 있고 길이가 짧은 경우 (1, 3, 4 같은 값)
        if date_str.isdigit() and len(date_str) < 8:
            raise ValueError(
                f"Invalid date format: '{date_str}' (numeric only, too short)"
            )

        # "22-03-11 10:00" 또는 "24-01-18 10:00" 형식 (YY-MM-DD HH:MM)
        if "-" in date_str and ":" in date_str:
            try:
                return datetime.strptime(date_str, "%y-%m-%d %H:%M")
            except ValueError as e:
                # 파싱 실패 시 구체적인 에러 메시지
                raise ValueError(
                    f"Cannot parse date '{date_str}' with format YY-MM-DD HH:MM: {str(e)}"
                )

        # "2024.1.18  10:00:00 AM" 형식
        if "." in date_str:
            try:
                # 중복 공백 제거
                date_str = " ".join(date_str.split())
                return datetime.strptime(date_str, "%Y.%m.%d %I:%M:%S %p")
            except ValueError:
                try:
                    return datetime.strptime(date_str, "%Y.%m.%d %H:%M:%S")
                except ValueError:
                    pass

        raise ValueError(f"Cannot parse date: '{date_str}' (unknown format)")

    @staticmethod
    def parse_integer(value: Any) -> int:
        """문자열이나 숫자를 정수로 변환

        쉼표가 포함된 문자열도 처리
        """
        if pd.isna(value):
            return 0

        if isinstance(value, (int, float)):
            return int(value)

        # 문자열인 경우 쉼표 제거
        value_str = str(value).replace(",", "").strip()

        try:
            return int(float(value_str))
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def parse_ratio(value: Any) -> float:
        """비율 값을 소수점 5자리로 반올림

        Args:
            value: 비율 값 (float 또는 문자열)

        Returns:
            소수점 5자리로 반올림된 float
        """
        if pd.isna(value):
            return 0.0

        if isinstance(value, (int, float)):
            return round(float(value), 5)

        try:
            return round(float(str(value).replace(",", "").strip()), 5)
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def parse_string(value: Any) -> str:
        """값을 문자열로 변환"""
        if pd.isna(value):
            return ""
        return str(value).strip()

    @staticmethod
    def parse_optional_float(value: Any) -> float | None:
        """선택적 float 값 파싱"""
        if pd.isna(value) or value == "":
            return None

        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def parse_optional_int(value: Any) -> int | None:
        """선택적 int 값 파싱

        '-' 같은 특수 문자는 None으로 처리
        """
        if pd.isna(value) or value == "" or value == "-":
            return None

        try:
            value_str = str(value).replace(",", "").strip()
            if not value_str or value_str == "-":
                return None
            return int(float(value_str))
        except (ValueError, TypeError):
            return None
