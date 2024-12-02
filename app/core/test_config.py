from pydantic_settings import BaseSettings

class TestSettings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@test_db:5432/test_db"
    API_V1_STR: str = "/api/v1"
    APP_NAME: str = "Todo API Test"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SECRET_KEY: str = "test_secret_key"

test_settings = TestSettings() 