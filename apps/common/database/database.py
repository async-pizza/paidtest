from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from settings import config

from .mixin import Base  # noqa

engine = create_async_engine(config.DATABASE_URL)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(bind=engine) as session:
        yield session
