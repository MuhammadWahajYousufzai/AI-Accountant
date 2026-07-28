from pydantic import BaseModel
from typing import Optional


class TransactionResponse(BaseModel):
    id: str
    type: str
    amount_cents: int
    currency: str
    description: str
    vendor_source: Optional[str] = None
    date: str
    category: Optional[dict] = None
    created_at: str


class PaginatedTransactions(BaseModel):
    items: list[TransactionResponse]
    total: int
    page: int
    per_page: int
    pages: int
