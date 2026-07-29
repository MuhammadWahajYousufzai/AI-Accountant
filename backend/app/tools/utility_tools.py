import json

from agents import function_tool


def get_all_categories_tool(get_db, get_user_id):
    @function_tool
    async def get_all_categories() -> str:
        """Get all categories the user has. Use this when you need to check if a category exists or show available categories."""
        from app.repositories.category_repo import CategoryRepository

        async with get_db() as db:
            repo = CategoryRepository(db)
            items = await repo.list(get_user_id())
            return json.dumps({
                "items": [
                    {"id": c.id, "name": c.name, "type": c.type}
                    for c in items
                ],
                "count": len(items),
            })

    return get_all_categories


def get_all_accounts_tool(get_db, get_user_id):
    @function_tool
    async def get_all_accounts() -> str:
        """Get all accounts for the user. Use this to show the user their accounts or when you need account info."""
        from app.repositories.account_repo import AccountRepository

        async with get_db() as db:
            repo = AccountRepository(db)
            items = await repo.list(get_user_id())
            return json.dumps({
                "items": [
                    {"id": a.id, "name": a.name, "type": a.currency}
                    for a in items
                ],
                "count": len(items),
            })

    return get_all_accounts


def get_total_income_tool(get_db, get_user_id):
    @function_tool
    async def get_total_income() -> str:
        """Get the total amount of all income records."""
        from app.repositories.income_repo import IncomeRepository
        from app.services.income_service import list_income as svc_list

        async with get_db() as db:
            items, total = await svc_list(db, get_user_id(), {}, 1, 10000)
            total_cents = sum(t.amount_cents for t in items)
            return json.dumps({
                "total_cents": total_cents,
                "count": total,
                "items": [
                    {"id": t.id, "amount_cents": t.amount_cents, "description": t.description, "date": str(t.date), "source": t.vendor_source}
                    for t in items
                ],
            })

    return get_total_income


def get_total_expense_tool(get_db, get_user_id):
    @function_tool
    async def get_total_expense() -> str:
        """Get the total amount of all expense records."""
        from app.services.expense_service import list_expenses as svc_list

        async with get_db() as db:
            items, total = await svc_list(db, get_user_id(), {}, 1, 10000)
            total_cents = sum(t.amount_cents for t in items)
            return json.dumps({
                "total_cents": total_cents,
                "count": total,
                "items": [
                    {"id": t.id, "amount_cents": t.amount_cents, "description": t.description, "date": str(t.date), "vendor": t.vendor_source}
                    for t in items
                ],
            })

    return get_total_expense
