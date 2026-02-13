from collections import defaultdict

from fastapi import (
    Depends,
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth.models import User
from apps.messages.models import Message
from core.deps import get_session

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
    ):
        await websocket.accept()
        if not active_connections.get(user.id):
            active_connections[user.id] = set()
        active_connections[user.id].add(websocket)
        try:
            while True:
                message = await websocket.receive_text()
                for user_id, connections in active_connections.items():
                    for conn in connections:
                        await conn.send_text(message)
        except WebSocketDisconnect as e:
            connections = active_connections.get(user.id)
            if connections:
                connections.discard(websocket)
                if not connections:
                    del active_connections[user.id]
