from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from redis.asyncio import Redis

from apps.messages.router import router as messages_router
from core.config import settings
from core.database import Database
from core.deps import get_redis, get_session
from core.models_base import Base
from core.redis import RedisService
from core.ws_registery import register_ws

templates = Jinja2Templates(directory="templates")


def create_app() -> FastAPI:
    database_url = settings.DATABASE_URL
    if not database_url:
        raise RuntimeError("Database url is not loaded from the environment variables")
    database = Database(database_url=database_url, echo=True)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("startup: performing lightweight app checks")
        async with database.engine.begin() as conn:
            from apps.auth.models import User
            from apps.messages.models import Message

            await conn.run_sync(Base.metadata.create_all)
        redis_service = RedisService()
        app.dependency_overrides[get_redis] = lambda: redis_service.client
        register_ws(app)
        print("startup COMPLETED")
        yield
        print("shutdown: cleaning up")
        await database.dispose()
        await redis_service.close()
        print("shutdown COMPLETED")

    app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
    app.dependency_overrides[get_session] = database.get_session
    app.include_router(messages_router)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()
