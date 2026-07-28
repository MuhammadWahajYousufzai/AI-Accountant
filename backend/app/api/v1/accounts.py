from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_authenticated_user
from app.schemas.account import AccountCreate, AccountResponse, AccountList
from app.repositories.account_repo import AccountRepository

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=AccountList)
async def list_accounts(auth: tuple[str, AsyncSession] = Depends(get_authenticated_user)):
    user_id, db = auth
    repo = AccountRepository(db)
    accounts = await repo.list(user_id)
    return {
        "items": [
            {"id": a.id, "name": a.name, "type": a.type, "balance_cents": 0, "is_system": a.is_system}
            for a in accounts
        ]
    }


@router.post("", response_model=AccountResponse, status_code=201)
async def create_account(
    req: AccountCreate,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    repo = AccountRepository(db)
    existing = await repo.get_by_name(user_id, req.name)
    if existing:
        raise HTTPException(status_code=409, detail="An account with this name already exists")
    account = await repo.create(user_id, req.name, req.type)
    return {"id": account.id, "name": account.name, "type": account.type, "balance_cents": 0, "is_system": account.is_system}
