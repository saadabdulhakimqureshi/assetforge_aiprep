from repositories.base import ReadRepo
from repositories.models import Asset
from sqlmodel import select


class AssetsRepo(ReadRepo):
    async def get_all(self) -> list[Asset]:
        return await self.get_many(Asset)

    async def get_by_category(self, category: str) -> list[Asset]:
        return await self.get_many(Asset, category=category)

    async def search(self, keyword: str) -> list[Asset]:
        like = f"%{keyword}%"
        async with self.session_factory() as session:
            query = select(Asset).where(
                Asset.name.like(like) |
                Asset.description.like(like) |
                Asset.tags.like(like)
            )
            result = await session.exec(query)
            return result.all()
