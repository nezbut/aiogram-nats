from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from aiogram_nats.infrastructure.database.rdb.models.base import Base, id_int


class UserORM(Base):

    """Represents a user in the database."""

    __tablename__ = "user"

    id: Mapped[id_int]
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    joined_us: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now(),
    )
