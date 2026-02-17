from typing import AsyncGenerator

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    raise RuntimeError("Database is not initialized")


def get_redis() -> Redis:
    raise RuntimeError("RedisService not initialized in the lifespan")
