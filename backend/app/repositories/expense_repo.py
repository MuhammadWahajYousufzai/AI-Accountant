from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction
from app.repositories.base import BaseRepository


class ExpenseRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def list(self, user_id: str, filters: dict, page: int = 1, per_page: int = 20):
        stmt = select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.type == "expense",
        )

        if filters.get("category_id"):
            stmt = stmt.where(Transaction.category_id == filters["category_id"])
        if filters.get("date_from"):
            stmt = stmt.where(Transaction.date >= filters["date_from"])
        if filters.get("date_to"):
            stmt = stmt.where(Transaction.date <= filters["date_to"])
        if filters.get("amount_min"):
            stmt = stmt.where(Transaction.amount_cents >= filters["amount_min"])
        if filters.get("amount_max"):
            stmt = stmt.where(Transaction.amount_cents <= filters["amount_max"])
        if filters.get("search"):
            search = f"%{filters['search']}%"
            stmt = stmt.where(
                Transaction.description.ilike(search) | Transaction.vendor_source.ilike(search)
            )

        total_stmt = select(stmt.subquery())
        total = await self.count(total_stmt)

        stmt = stmt.order_by(Transaction.date.desc()).offset((page - 1) * per_page).limit(per_page)
        result = await self.db.execute(stmt)
        items = result.scalars().all()

        return items, total

    async def get(self, user_id: str, expense_id: str) -> Transaction | None:
        stmt = select(Transaction).where(
            Transaction.id == expense_id,
            Transaction.user_id == user_id,
            Transaction.type == "expense",
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> Transaction:
        txn = Transaction(type="expense", **kwargs)
        self.db.add(txn)
        await self.db.flush()
        return txn

    async def update(self, txn: Transaction, **kwargs) -> Transaction:
        for key, value in kwargs.items():
            setattr(txn, key, value)
        await self.db.flush()
        return txn

    async def delete(self, txn: Transaction):
        await self.db.delete(txn)
        await self.db.flush()
