from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_authenticated_user
from app.schemas.report import ProfitLossRequest, ProfitLossResponse, BalanceSheetRequest, BalanceSheetResponse, DashboardSummary
from app.services.report_service import generate_profit_loss, generate_balance_sheet, get_dashboard_summary

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/profit-loss", response_model=ProfitLossResponse)
async def profit_loss(
    req: ProfitLossRequest,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    return await generate_profit_loss(db, user_id, req.date_from, req.date_to)


@router.post("/balance-sheet", response_model=BalanceSheetResponse)
async def balance_sheet(
    req: BalanceSheetRequest,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    return await generate_balance_sheet(db, user_id, req.as_of_date)


@router.get("/dashboard", response_model=DashboardSummary)
async def dashboard(
    month: str | None = None,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    return await get_dashboard_summary(db, user_id, month)
