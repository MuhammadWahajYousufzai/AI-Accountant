from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction
from app.repositories.base import BaseRepository


class TransactionRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def list_with_filters(self, user_id: str, filters: dict, page: int = 1, per_page: int = 20):
        stmt = select(Transaction).where(Transaction.user_id == user_id)

        if filters.get("type"):
            stmt = stmt.where(Transaction.type == filters["type"])
        if filters.get("date_from"):
            stmt = stmt.where(Transaction.date >= filters["date_from"])
        if filters.get("date_to"):
            stmt = stmt.where(Transaction.date <= filters["date_to"])
        if filters.get("category_id"):
            stmt = stmt.where(Transaction.category_id == filters["category_id"])
        if filters.get("search"):
            search = f"%{filters['search']}%"
            stmt = stmt.where(
                Transaction.description.ilike(search) | Transaction.vendor_source.ilike(search)
            )

        total = await self.count(select(stmt.subquery()))

        stmt = stmt.order_by(Transaction.date.desc()).offset((page - 1) * per_page).limit(per_page)
        result = await self.db.execute(stmt)
        items = result.scalars().all()

        return items, total

    async def search(self, user_id: str, query: str, limit: int = 20):
        search = f"%{query}%"
        stmt = (
            select(Transaction)
            .where(
                Transaction.user_id == user_id,
                Transaction.description.ilike(search) | Transaction.vendor_source.ilike(search),
            )
            .order_by(Transaction.date.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_range(self, user_id: str, date_from: str, date_to: str):
        stmt = select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.date >= date_from,
            Transaction.date <= date_to,
        ).order_by(Transaction.date)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_all(self, user_id: str):
        stmt = select(Transaction).where(Transaction.user_id == user_id).order_by(Transaction.date)
        result = await self.db.execute(stmt)
        return result.scalars().all()
