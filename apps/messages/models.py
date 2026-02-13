from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models_base import Base, IdMixin, TimestampMixin

if TYPE_CHECKING:
    from apps.auth.models import User


class Message(Base, IdMixin, TimestampMixin):
    __tablename__ = "messages"
    content: Mapped[str] = mapped_column(Text, nullable=False)
    sender_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    sender: Mapped["User"] = relationship(back_populates="messages", lazy="selectin")
