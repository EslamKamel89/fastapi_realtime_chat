from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.messages.models import Message


class MessageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: int, content: str) -> Message:
        message = Message(sender_id=user_id, content=content)
        self.session.add(message)
        await self.session.flush()
        await self.session.refresh(message)
        await self.session.commit()
        return message

    async def all(self) -> Sequence[Message]:
        res = await self.session.execute(select(Message))
        return res.scalars().all()
