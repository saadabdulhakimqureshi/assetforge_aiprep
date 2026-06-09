from sqlmodel import SQLModel, select
from typing import Type, TypeVar
from database import AsyncSessionLocal

T = TypeVar("T", bound=SQLModel)


class ReadRepo:
    def __init__(self):
        self.session_factory = AsyncSessionLocal

    async def get_one(self, model: Type[T], **filters) -> T | None:
        async with self.session_factory() as session:
            query = select(model)
            for key, value in filters.items():
                query = query.where(getattr(model, key) == value)
            result = await session.exec(query)
            return result.first()

    async def get_many(self, model: Type[T], **filters) -> list[T]:
        async with self.session_factory() as session:
            query = select(model)
            for key, value in filters.items():
                query = query.where(getattr(model, key) == value)
            result = await session.exec(query)
            return result.all()


class ReadWriteRepo(ReadRepo):
    async def create(self, instance: SQLModel) -> SQLModel:
        async with self.session_factory() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def create_many(self, instances: list[SQLModel]) -> None:
        async with self.session_factory() as session:
            for instance in instances:
                session.add(instance)
            await session.commit()

    async def update(self, instance: SQLModel) -> SQLModel:
        async with self.session_factory() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def delete(self, instance: SQLModel) -> None:
        async with self.session_factory() as session:
            await session.delete(instance)
            await session.commit()
