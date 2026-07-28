from math import ceil

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_authenticated_user
from app.schemas.transaction import TransactionResponse, PaginatedTransactions
from app.repositories.transaction_repo import TransactionRepository

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=PaginatedTransactions)
async def list_transactions(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    type: str | None = None,
    category_id: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    search: str | None = None,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    filters = {k: v for k, v in locals().items() if k not in ("user_id", "db", "page", "per_page", "auth") and v is not None}
    repo = TransactionRepository(db)
    items, total = await repo.list_with_filters(user_id, filters, page, per_page)

    return {
        "items": [
            {
                "id": t.id,
                "type": t.type,
                "amount_cents": t.amount_cents,
                "currency": t.currency,
                "description": t.description,
                "vendor_source": t.vendor_source,
                "date": str(t.date),
                "category": {"id": t.category_id, "name": t.category_id} if t.category_id else None,
                "created_at": str(t.created_at),
            }
            for t in items
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": ceil(total / per_page) if total else 0,
    }
