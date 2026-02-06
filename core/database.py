from typing import AsyncGenerator, Final

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class Database:
    def __init__(self, *, database_url: str, echo: bool = False) -> None:
        self.database_url: Final[str] = database_url
        self.engine: AsyncEngine = create_async_engine(
            database_url,
            echo=echo,
            future=True,
        )
        self.SessionLocal = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
            class_=AsyncSession,
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.SessionLocal() as session:
            yield session

    async def dispose(self):
        await self.engine.dispose()
