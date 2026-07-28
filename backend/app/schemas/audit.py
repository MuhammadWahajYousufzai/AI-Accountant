from pydantic import BaseModel
from typing import Optional


class AuditRunRequest(BaseModel):
    period_start: str
    period_end: str


class FindingResponse(BaseModel):
    type: str
    severity: str
    transaction_id: Optional[str] = None
    description: str


class AuditRunResponse(BaseModel):
    id: str
    period: dict
    status: str
    findings: list[FindingResponse]
    summary: str
    disclaimer: str
