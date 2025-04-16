from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-here"  # Change this in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 300

    class Config:
        env_file = ".env"


settings = Settings()
