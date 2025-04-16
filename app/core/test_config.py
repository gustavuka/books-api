from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    TEST_DATABASE_URL: str = "sqlite:///test_db.db"
    SECRET_KEY: str = "test-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


test_settings = TestSettings()
