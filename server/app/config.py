from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./data.db"
    API_PREFIX: str = "/api"
    ALLOW_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
