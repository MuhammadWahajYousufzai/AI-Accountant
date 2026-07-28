from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.expense_repo import ExpenseRepository
from app.repositories.category_repo import CategoryRepository
from app.repositories.account_repo import AccountRepository


async def create_expense(
    db: AsyncSession,
    user_id: str,
    amount_cents: int,
    description: str,
    date: str,
    currency: str = "GBP",
    vendor: str | None = None,
    category_name: str | None = None,
    account_name: str | None = None,
):
    cat_repo = CategoryRepository(db)
    acc_repo = AccountRepository(db)

    category_id = None
    if category_name:
        cat = await cat_repo.get_by_name(user_id, category_name, "expense")
        if cat:
            category_id = cat.id

    account_id = None
    if account_name:
        acc = await acc_repo.get_by_name(user_id, account_name)
        if acc:
            account_id = acc.id
    else:
        cash = await acc_repo.get_by_name(user_id, "Cash")
        if cash:
            account_id = cash.id

    expense_repo = ExpenseRepository(db)
    txn = await expense_repo.create(
        user_id=user_id,
        amount_cents=amount_cents,
        currency=currency,
        description=description,
        vendor_source=vendor,
        date=date,
        category_id=category_id,
        account_id=account_id,
    )

    return txn


async def list_expenses(db: AsyncSession, user_id: str, filters: dict, page: int = 1, per_page: int = 20):
    repo = ExpenseRepository(db)
    return await repo.list(user_id, filters, page, per_page)


async def get_expense(db: AsyncSession, user_id: str, expense_id: str):
    repo = ExpenseRepository(db)
    return await repo.get(user_id, expense_id)


async def update_expense(db: AsyncSession, user_id: str, expense_id: str, updates: dict):
    repo = ExpenseRepository(db)
    txn = await repo.get(user_id, expense_id)
    if not txn:
        return None

    if "category_name" in updates and updates["category_name"]:
        cat_repo = CategoryRepository(db)
        cat = await cat_repo.get_by_name(user_id, updates.pop("category_name"), "expense")
        if cat:
            updates["category_id"] = cat.id

    if "vendor" in updates:
        updates["vendor_source"] = updates.pop("vendor")

    return await repo.update(txn, **updates)


async def delete_expense(db: AsyncSession, user_id: str, expense_id: str) -> bool:
    repo = ExpenseRepository(db)
    txn = await repo.get(user_id, expense_id)
    if not txn:
        return False
    await repo.delete(txn)
    return True
