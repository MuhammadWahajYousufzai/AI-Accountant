from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_authenticated_user
from app.schemas.audit import AuditRunRequest, AuditRunResponse
from app.services.audit_service import run_audit

router = APIRouter(prefix="/audit", tags=["audit"])


@router.post("/run", response_model=AuditRunResponse)
async def run_monthly_audit(
    req: AuditRunRequest,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    return await run_audit(db, user_id, req.period_start, req.period_end)
