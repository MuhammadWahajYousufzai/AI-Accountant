import json

from agents import function_tool


def create_expense_tool(get_db, get_user_id):
    @function_tool
    async def create_expense(
        amount_cents: int,
        description: str,
        date: str,
        category_name: str | None = None,
        vendor: str | None = None,
        account_name: str | None = None,
    ) -> str:
        """Create a new expense transaction. Amount is in cents (1 pound = 100 pence). If vendor is not provided, it will be set to 'General'."""
        from app.services.expense_service import create_expense as svc_create

        async with get_db() as db:
            txn = await svc_create(
                db, get_user_id(), amount_cents, description, date,
                vendor=vendor, category_name=category_name, account_name=account_name,
            )
            result = {
                "id": txn.id,
                "amount_cents": txn.amount_cents,
                "description": txn.description,
                "date": str(txn.date),
                "vendor": txn.vendor_source,
                "category": category_name,
            }
            return json.dumps(result)

    return create_expense


def list_expenses_tool(get_db, get_user_id):
    @function_tool
    async def list_expenses(
        category_name: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        search: str | None = None,
        page: int = 1,
        per_page: int = 50,
    ) -> str:
        """List expenses with optional filters. Use this to get all expenses or filter by category/date range."""
        from app.services.expense_service import list_expenses as svc_list

        filters = {}
        if category_name:
            from app.repositories.category_repo import CategoryRepository
            async with get_db() as db:
                repo = CategoryRepository(db)
                cat = await repo.get_by_name(get_user_id(), category_name, "expense")
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
                    {"id": t.id, "amount_cents": t.amount_cents, "description": t.description, "date": str(t.date), "vendor": t.vendor_source}
                    for t in items
                ],
                "total": total,
                "page": page,
                "per_page": per_page,
            }
            return json.dumps(result)

    return list_expenses


def get_expense_tool(get_db, get_user_id):
    @function_tool
    async def get_expense(expense_id: str) -> str:
        """Get a single expense by its ID."""
        from app.services.expense_service import get_expense as svc_get

        async with get_db() as db:
            txn = await svc_get(db, get_user_id(), expense_id)
            if not txn:
                return json.dumps({"error": "Expense not found"})
            return json.dumps({
                "id": txn.id,
                "amount_cents": txn.amount_cents,
                "description": txn.description,
                "date": str(txn.date),
                "vendor": txn.vendor_source,
                "category_id": txn.category_id,
            })

    return get_expense


def update_expense_tool(get_db, get_user_id):
    @function_tool
    async def update_expense(
        expense_id: str,
        amount_cents: int | None = None,
        description: str | None = None,
        date: str | None = None,
        category_name: str | None = None,
        vendor: str | None = None,
    ) -> str:
        """Update an existing expense. Only provided fields will be updated."""
        from app.services.expense_service import update_expense as svc_update

        updates = {}
        if amount_cents is not None:
            updates["amount_cents"] = amount_cents
        if description:
            updates["description"] = description
        if date:
            updates["date"] = date
        if category_name:
            updates["category_name"] = category_name
        if vendor:
            updates["vendor"] = vendor

        async with get_db() as db:
            txn = await svc_update(db, get_user_id(), expense_id, updates)
            if not txn:
                return json.dumps({"error": "Expense not found"})
            return json.dumps({
                "id": txn.id,
                "amount_cents": txn.amount_cents,
                "description": txn.description,
                "date": str(txn.date),
                "vendor": txn.vendor_source,
            })

    return update_expense


def delete_expense_tool(get_db, get_user_id):
    @function_tool
    async def delete_expense(expense_id: str) -> str:
        """Delete an expense by its ID. Only call this after the user explicitly confirms deletion."""
        from app.services.expense_service import delete_expense as svc_delete

        async with get_db() as db:
            success = await svc_delete(db, get_user_id(), expense_id)
            return json.dumps({"success": success, "deleted": success})

    return delete_expense
