import json

from agents import function_tool


def search_transactions_tool(get_db, get_user_id):
    @function_tool
    async def search_transactions(
        query: str,
        date_from: str | None = None,
        date_to: str | None = None,
        type: str | None = None,
        limit: int = 20,
    ) -> str:
        """Search across all transactions by description or vendor/source. Optionally filter by date range and type (expense/income)."""
        from app.repositories.transaction_repo import TransactionRepository

        filters = {}
        if date_from:
            filters["date_from"] = date_from
        if date_to:
            filters["date_to"] = date_to
        if type:
            filters["type"] = type
        filters["search"] = query

        async with get_db() as db:
            repo = TransactionRepository(db)
            items, _ = await repo.list_with_filters(get_user_id(), filters, page=1, per_page=limit)
            result = {
                "items": [
                    {
                        "id": t.id,
                        "type": t.type,
                        "amount_cents": t.amount_cents,
                        "description": t.description,
                        "vendor_source": t.vendor_source,
                        "date": str(t.date),
                    }
                    for t in items
                ],
                "count": len(items),
            }
            return json.dumps(result)

    return search_transactions
