from datetime import datetime

from sqlalchemy import ForeignKey, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from apps.common.database import Base


class Call(Base):
    __tablename__ = "calls"

    duration: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    call_type: Mapped[str]
    date: Mapped[datetime]
    mark: Mapped[int]
    call_text: Mapped[str]

    @classmethod
    async def get_total_score(cls, session: AsyncSession, user_id: int) -> int:
        score = await session.scalar(
            select(func.sum(cls.mark)).where(cls.user_id == user_id)
        )
        return score or 0
