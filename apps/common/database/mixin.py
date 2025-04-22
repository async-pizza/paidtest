from typing import Type, TypeVar

from fastapi import HTTPException
from sqlalchemy import (
    ColumnExpressionArgument,
    ScalarResult,
    Select,
    delete,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

T = TypeVar("T", bound="Base")
ValueT = TypeVar("ValueT")


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @classmethod
    async def create(
        cls: Type[T], session: AsyncSession, **values: ValueT
    ) -> T:
        instance = cls(**values)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    @classmethod
    async def get_or_none(
        cls: Type[T], session: AsyncSession, object_id: int
    ) -> T | None:
        search = cls.id == object_id
        result: T | None = await session.scalar(select(cls).filter(search))
        return result

    @classmethod
    async def get(cls: Type[T], session: AsyncSession, object_id: int) -> T:
        result: T | None = await cls.get_or_none(session, object_id)
        if not result:
            raise HTTPException(
                status_code=404, detail=f"{cls.__name__} not found"
            )
        return result

    @classmethod
    async def first_or_none(
        cls: Type[T], session: AsyncSession, search: ColumnExpressionArgument
    ) -> T | None:
        query: Select = select(cls).where(search)
        result: T | None = await session.scalar(query)
        return result

    @classmethod
    async def first(
        cls: Type[T], session: AsyncSession, search: ColumnExpressionArgument
    ) -> T:
        result = await cls.first_or_none(session, search)
        if not result:
            raise HTTPException(
                status_code=404, detail=f"{cls.__name__} not found"
            )
        return result

    @classmethod
    async def all(
        cls: Type[T],
        session: AsyncSession,
        search: ColumnExpressionArgument | None = None,
    ) -> list[T]:
        query: Select = select(cls)
        if search is not None:
            query = query.where(search)
        scalar_result: ScalarResult[T] = await session.scalars(query)
        return list(scalar_result.all())

    async def update(self: T, session: AsyncSession, **values: ValueT) -> T:
        for key, value in values.items():
            setattr(self, key, value)
        session.add(self)
        await session.commit()
        await session.refresh(self)
        return self

    async def delete(self: T, session: AsyncSession) -> None:
        search = self.__class__.id == self.id
        await session.execute(delete(self.__class__).where(search))
        await session.commit()
