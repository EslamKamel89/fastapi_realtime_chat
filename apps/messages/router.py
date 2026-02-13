from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

import core.main as main
from apps.messages.repository import MessageRepository
from core.deps import get_session

router = APIRouter(prefix="", tags=["home"])


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, session: AsyncSession = Depends(get_session)):
    repo = MessageRepository(session)
    messages = await repo.all()
    serialized = [
        {
            "id": message.id,
            "content": message.content,
            "sender": {
                "id": message.sender.id,
                "username": message.sender.username,
                "email": message.sender.email,
            },
        }
        for message in messages
    ]
    return main.templates.TemplateResponse(
        request, "index.html", {"messages": serialized}
    )
