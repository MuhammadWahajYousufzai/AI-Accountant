from pydantic import BaseModel
from typing import Optional


class ProfitLossRequest(BaseModel):
    date_from: str
    date_to: str


class BreakdownItem(BaseModel):
    category: str
    amount_cents: int
    percentage: float


class ProfitLossResponse(BaseModel):
    period: dict
    total_income_cents: int
    total_expense_cents: int
    net_profit_cents: int
    currency: str
    expense_breakdown: list[BreakdownItem]
    income_breakdown: list[BreakdownItem]


class BalanceSheetRequest(BaseModel):
    as_of_date: str


class BalanceSheetItem(BaseModel):
    account: str
    amount_cents: int


class BalanceSheetResponse(BaseModel):
    as_of_date: str
    total_assets_cents: int
    total_liabilities_cents: int
    total_equity_cents: int
    assets: list[BalanceSheetItem]
    liabilities: list[BalanceSheetItem]
    equity: list[BalanceSheetItem]


class DashboardSummary(BaseModel):
    total_income_cents: int
    total_expense_cents: int
    net_profit_cents: int
    cash_position_cents: int
    monthly_income: list[dict]
    monthly_expenses: list[dict]
    recent_transactions: list[dict]
    category_breakdown: list[dict]
    ai_insights: str
