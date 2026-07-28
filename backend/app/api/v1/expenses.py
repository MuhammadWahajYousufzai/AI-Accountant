from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_authenticated_user
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse, PaginatedExpenses
from app.services import expense_service

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("", response_model=PaginatedExpenses)
async def list_expenses(
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
    items, total = await expense_service.list_expenses(db, user_id, filters, page, per_page)

    return {
        "items": [_expense_to_response(e) for e in items],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": ceil(total / per_page) if total else 0,
    }


@router.post("", response_model=ExpenseResponse, status_code=201)
async def create_expense(
    req: ExpenseCreate,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    txn = await expense_service.create_expense(
        db, user_id, req.amount_cents, req.description, req.date,
        req.currency, req.vendor, req.category_name, req.account_name,
    )
    return _expense_to_response(txn)


@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(
    expense_id: str,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    txn = await expense_service.get_expense(db, user_id, expense_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Expense not found")
    return _expense_to_response(txn)


@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: str,
    req: ExpenseUpdate,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    updates = req.model_dump(exclude_unset=True)
    txn = await expense_service.update_expense(db, user_id, expense_id, updates)
    if not txn:
        raise HTTPException(status_code=404, detail="Expense not found")
    return _expense_to_response(txn)


@router.delete("/{expense_id}", status_code=204)
async def delete_expense(
    expense_id: str,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    deleted = await expense_service.delete_expense(db, user_id, expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")


def _expense_to_response(txn):
    return {
        "id": txn.id,
        "amount_cents": txn.amount_cents,
        "currency": txn.currency,
        "description": txn.description,
        "vendor": txn.vendor_source,
        "date": str(txn.date),
        "category": {"id": txn.category_id, "name": txn.category_id} if txn.category_id else None,
        "account": {"id": txn.account_id, "name": txn.account_id} if txn.account_id else None,
        "is_reconciled": txn.is_reconciled,
        "created_at": str(txn.created_at),
    }
