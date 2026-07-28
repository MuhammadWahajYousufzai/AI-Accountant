from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def list(self, user_id: str):
        stmt = select(Category).where(Category.user_id == user_id).order_by(Category.name)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_name(self, user_id: str, name: str, type: str) -> Category | None:
        stmt = select(Category).where(
            Category.user_id == user_id,
            Category.name == name,
            Category.type == type,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get(self, category_id: str) -> Category | None:
        stmt = select(Category).where(Category.id == category_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user_id: str, name: str, type: str, is_system: bool = False) -> Category:
        cat = Category(user_id=user_id, name=name, type=type, is_system=is_system)
        self.db.add(cat)
        await self.db.flush()
        return cat
