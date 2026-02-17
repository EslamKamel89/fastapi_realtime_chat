import json
from collections import defaultdict

from fastapi import (
    Depends,
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth.models import User
from apps.messages.models import Message
from apps.messages.repository import MessageRepository
from core.deps import get_redis, get_session

active_connections: dict[int, set[WebSocket]] = defaultdict(set)


async def get_current_user(
    websocket: WebSocket,
    session: AsyncSession = Depends(get_session),
):
    email = websocket.query_params.get("email")
    if not email:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    res = await session.execute(select(User).where(User.email == email))
    user = res.scalar_one_or_none()
    if not user:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return user


def register_ws(app: FastAPI) -> None:
    @app.websocket("/ws")
    async def websocket_endpoint(
        websocket: WebSocket,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user),
        redis: Redis = Depends(get_redis),
    ):
        await websocket.accept()
        if not active_connections.get(user.id):
            active_connections[user.id] = set()
        active_connections[user.id].add(websocket)
        message_repo = MessageRepository(session)
        try:
            while True:
                message = await websocket.receive_text()
                message_obj = await message_repo.create(user.id, message)
                serialized = {
                    "id": message_obj.id,
                    "content": message_obj.content,
                    "sender": {
                        "id": message_obj.sender.id,
                        "username": message_obj.sender.username,
                        "email": message_obj.sender.email,
                    },
                }
                await redis.publish(
                    "chat_messages",
                    json.dumps(serialized),
                )
                # for user_id, connections in active_connections.items():
                #     for conn in connections:
                #         await conn.send_text(json.dumps(serialized))
        except WebSocketDisconnect as e:
            connections = active_connections.get(user.id)
            if connections:
                connections.discard(websocket)
                if not connections:
                    del active_connections[user.id]
