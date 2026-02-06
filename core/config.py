import os

from pydantic import BaseModel


class Settings(BaseModel):
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI app")
    DATABASE_URL: str | None = os.getenv("DATABASE_URL", None)


settings = Settings()
