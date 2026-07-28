from pydantic import BaseModel, Field
from typing import Optional


class ExpenseCreate(BaseModel):
    amount_cents: int = Field(..., gt=0)
    currency: str = "GBP"
    description: str
    vendor: Optional[str] = None
    date: str
    category_name: Optional[str] = None
    account_name: Optional[str] = None


class ExpenseUpdate(BaseModel):
    amount_cents: Optional[int] = Field(None, gt=0)
    currency: Optional[str] = None
    description: Optional[str] = None
    vendor: Optional[str] = None
    date: Optional[str] = None
    category_name: Optional[str] = None
    account_name: Optional[str] = None


class CategoryRef(BaseModel):
    id: str
    name: str


class AccountRef(BaseModel):
    id: str
    name: str


class ExpenseResponse(BaseModel):
    id: str
    amount_cents: int
    currency: str
    description: str
    vendor: Optional[str] = None
    date: str
    category: Optional[CategoryRef] = None
    account: Optional[AccountRef] = None
    is_reconciled: bool
    created_at: str


class PaginatedExpenses(BaseModel):
    items: list[ExpenseResponse]
    total: int
    page: int
    per_page: int
    pages: int
