from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models_base import Base, IdMixin, TimestampMixin

if TYPE_CHECKING:
    from apps.messages.models import Message


class User(Base, IdMixin, TimestampMixin):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True,
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="sender", lazy="selectin"
    )
