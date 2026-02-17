import os

from dotenv import load_dotenv

load_dotenv()

from pydantic import BaseModel


class Settings(BaseModel):
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI app")
    DATABASE_URL: str | None = os.getenv("DATABASE_URL", None)
    REDIS_HOST: str | None = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT: int | None = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int | None = int(os.getenv("REDIS_DB", 0))


settings = Settings()
