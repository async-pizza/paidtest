from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.calls.models import Call
from apps.common.database import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    calls: Mapped[list[Call]] = relationship()
