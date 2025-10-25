from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    MONGO_DB_URL: str
    MODE: str
    OPENAPI_API_KEY: str

    model_config = ConfigDict(env_file=".env", extra="ignore")


# 환경 설정을 인스턴스로 가져오기
settings = Settings()  # type: ignore
