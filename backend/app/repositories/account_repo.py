from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.repositories.base import BaseRepository


class AccountRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def list(self, user_id: str):
        stmt = select(Account).where(Account.user_id == user_id).order_by(Account.name)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_name(self, user_id: str, name: str) -> Account | None:
        stmt = select(Account).where(Account.user_id == user_id, Account.name == name)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get(self, account_id: str) -> Account | None:
        stmt = select(Account).where(Account.id == account_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user_id: str, name: str, type: str, is_system: bool = False) -> Account:
        account = Account(user_id=user_id, name=name, type=type, is_system=is_system)
        self.db.add(account)
        await self.db.flush()
        return account
