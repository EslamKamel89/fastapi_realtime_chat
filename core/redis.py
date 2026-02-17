from redis.asyncio import Redis

from core.config import settings


class RedisService:

    def __init__(self) -> None:
        redis_host = settings.REDIS_HOST
        redis_port = settings.REDIS_PORT
        redis_db = settings.REDIS_DB

        if redis_host is None or redis_port is None or redis_db is None:
            raise RuntimeError(
                "Redis connection info is not set in the environment variables."
            )

        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self._client = Redis(
            host=self.redis_host,
            port=self.redis_port,
            db=self.redis_db,
            decode_responses=True,
        )

    @property
    def client(self) -> Redis:
        return self._client

    async def close(self) -> None:
        return await self._client.close()
