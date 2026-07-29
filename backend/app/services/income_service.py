from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.income_repo import IncomeRepository
from app.repositories.category_repo import CategoryRepository
from app.repositories.account_repo import AccountRepository


async def create_income(
    db: AsyncSession,
    user_id: str,
    amount_cents: int,
    description: str,
    date: str,
    currency: str = "GBP",
    source: str | None = None,
    category_name: str | None = None,
    account_name: str | None = None,
):
    cat_repo = CategoryRepository(db)
    acc_repo = AccountRepository(db)

    category_id = None
    if category_name:
        cat = await cat_repo.get_by_name(user_id, category_name, "income")
        if cat:
            category_id = cat.id

    account_id = None
    if account_name:
        acc = await acc_repo.get_by_name(user_id, account_name)
        if acc:
            account_id = acc.id
    else:
        bank = await acc_repo.get_by_name(user_id, "Bank Account")
        if bank:
            account_id = bank.id
        else:
            bank = await acc_repo.create(user_id, "Bank Account", "checking", is_system=True)
            account_id = bank.id

    income_repo = IncomeRepository(db)
    txn = await income_repo.create(
        user_id=user_id,
        amount_cents=amount_cents,
        currency=currency,
        description=description,
        vendor_source=source,
        date=date,
        category_id=category_id,
        account_id=account_id,
    )

    return txn


async def list_income(db: AsyncSession, user_id: str, filters: dict, page: int = 1, per_page: int = 20):
    repo = IncomeRepository(db)
    return await repo.list(user_id, filters, page, per_page)


async def get_income(db: AsyncSession, user_id: str, income_id: str):
    repo = IncomeRepository(db)
    return await repo.get(user_id, income_id)


async def update_income(db: AsyncSession, user_id: str, income_id: str, updates: dict):
    repo = IncomeRepository(db)
    txn = await repo.get(user_id, income_id)
    if not txn:
        return None

    if "category_name" in updates and updates["category_name"]:
        cat_repo = CategoryRepository(db)
        cat = await cat_repo.get_by_name(user_id, updates.pop("category_name"), "income")
        if cat:
            updates["category_id"] = cat.id

    if "source" in updates:
        updates["vendor_source"] = updates.pop("source")

    return await repo.update(txn, **updates)


async def delete_income(db: AsyncSession, user_id: str, income_id: str) -> bool:
    repo = IncomeRepository(db)
    txn = await repo.get(user_id, income_id)
    if not txn:
        return False
    await repo.delete(txn)
    return True
