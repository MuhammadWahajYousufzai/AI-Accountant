from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def count(self, stmt) -> int:
        count_stmt = select(func.count()).select_from(stmt.subquery())
        result = await self.db.execute(count_stmt)
        return result.scalar_one()
