from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_authenticated_user
from app.schemas.report import DashboardSummary
from app.services.report_service import get_dashboard_summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
async def dashboard_summary(
    month: str | None = None,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    return await get_dashboard_summary(db, user_id, month)
