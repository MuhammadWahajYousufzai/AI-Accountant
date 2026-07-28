from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_authenticated_user
from app.schemas.income import IncomeCreate, IncomeUpdate, IncomeResponse, PaginatedIncome
from app.services import income_service

router = APIRouter(prefix="/income", tags=["income"])


@router.get("", response_model=PaginatedIncome)
async def list_income(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category_id: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    amount_min: int | None = None,
    amount_max: int | None = None,
    search: str | None = None,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    filters = {k: v for k, v in locals().items() if k not in ("user_id", "db", "page", "per_page", "auth") and v is not None}
    items, total = await income_service.list_income(db, user_id, filters, page, per_page)

    return {
        "items": [_income_to_response(e) for e in items],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": ceil(total / per_page) if total else 0,
    }


@router.post("", response_model=IncomeResponse, status_code=201)
async def create_income(
    req: IncomeCreate,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    txn = await income_service.create_income(
        db, user_id, req.amount_cents, req.description, req.date,
        req.currency, req.source, req.category_name, req.account_name,
    )
    return _income_to_response(txn)


@router.get("/{income_id}", response_model=IncomeResponse)
async def get_income(
    income_id: str,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    txn = await income_service.get_income(db, user_id, income_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Income not found")
    return _income_to_response(txn)


@router.put("/{income_id}", response_model=IncomeResponse)
async def update_income(
    income_id: str,
    req: IncomeUpdate,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    updates = req.model_dump(exclude_unset=True)
    txn = await income_service.update_income(db, user_id, income_id, updates)
    if not txn:
        raise HTTPException(status_code=404, detail="Income not found")
    return _income_to_response(txn)


@router.delete("/{income_id}", status_code=204)
async def delete_income(
    income_id: str,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    deleted = await income_service.delete_income(db, user_id, income_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Income not found")


def _income_to_response(txn):
    return {
        "id": txn.id,
        "amount_cents": txn.amount_cents,
        "currency": txn.currency,
        "description": txn.description,
        "source": txn.vendor_source,
        "date": str(txn.date),
        "category": {"id": txn.category_id, "name": txn.category_id} if txn.category_id else None,
        "account": {"id": txn.account_id, "name": txn.account_id} if txn.account_id else None,
        "is_reconciled": txn.is_reconciled,
        "created_at": str(txn.created_at),
    }
