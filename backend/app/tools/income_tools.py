import json

from agents import function_tool


def create_income_tool(get_db, get_user_id):
    @function_tool
    async def create_income(
        amount_cents: int,
        description: str,
        date: str,
        category_name: str | None = None,
        source: str | None = None,
        account_name: str | None = None,
    ) -> str:
        """Create a new income transaction. Amount is in cents (e.g., £1000 = 100000 pence). If source is not provided, it will be set to 'General'. Category will be auto-created if it doesn't exist."""
        from app.services.income_service import create_income as svc_create

        async with get_db() as db:
            txn = await svc_create(
                db, get_user_id(), amount_cents, description, date,
                source=source, category_name=category_name, account_name=account_name,
            )
            result = {
                "id": txn.id,
                "amount_cents": txn.amount_cents,
                "description": txn.description,
                "date": str(txn.date),
                "source": txn.vendor_source,
                "category": category_name,
            }
            return json.dumps(result)

    return create_income


def list_income_tool(get_db, get_user_id):
    @function_tool
    async def list_income(
        category_name: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        search: str | None = None,
        page: int = 1,
        per_page: int = 50,
    ) -> str:
        """List income records with optional filters. Use this to get all income or filter by category/date range/source."""
        from app.services.income_service import list_income as svc_list

        filters = {}
        if category_name:
            from app.repositories.category_repo import CategoryRepository
            async with get_db() as db:
                repo = CategoryRepository(db)
                cat = await repo.get_by_name(get_user_id(), category_name, "income")
                if cat:
                    filters["category_id"] = cat.id
        if date_from:
            filters["date_from"] = date_from
        if date_to:
            filters["date_to"] = date_to
        if search:
            filters["search"] = search

        async with get_db() as db:
            items, total = await svc_list(db, get_user_id(), filters, page, per_page)
            result = {
                "items": [
                    {"id": t.id, "amount_cents": t.amount_cents, "description": t.description, "date": str(t.date), "source": t.vendor_source}
                    for t in items
                ],
                "total": total,
                "page": page,
                "per_page": per_page,
            }
            return json.dumps(result)

    return list_income


def delete_income_tool(get_db, get_user_id):
    @function_tool
    async def delete_income(income_id: str) -> str:
        """Delete an income record by its ID. Only call this after the user explicitly confirms deletion."""
        from app.services.income_service import delete_income as svc_delete

        async with get_db() as db:
            success = await svc_delete(db, get_user_id(), income_id)
            return json.dumps({"success": success, "deleted": success})

    return delete_income
