import json

from agents import function_tool


def run_monthly_audit_tool(get_db, get_user_id):
    @function_tool
    async def run_monthly_audit(period_start: str, period_end: str) -> str:
        """Run an audit for the specified period (YYYY-MM-DD to YYYY-MM-DD). Checks for duplicates, missing info, unusual amounts, and categorization issues."""
        from app.services.audit_service import run_audit

        async with get_db() as db:
            result = await run_audit(db, get_user_id(), period_start, period_end)
            return json.dumps(result)

    return run_monthly_audit


def analyse_spending_tool(get_db, get_user_id):
    @function_tool
    async def analyse_spending(date_from: str | None = None, date_to: str | None = None) -> str:
        """Analyse spending patterns for a period. Shows category breakdown and identifies anomalies."""
        from app.services.report_service import generate_profit_loss

        async with get_db() as db:
            pl = await generate_profit_loss(db, get_user_id(), date_from or "1970-01-01", date_to or "2099-12-31")
            return json.dumps({
                "period": pl["period"],
                "total_expense_cents": pl["total_expense_cents"],
                "expense_breakdown": pl["expense_breakdown"],
                "insight": f"Highest expense category: {pl['expense_breakdown'][0]['category'] if pl['expense_breakdown'] else 'None'}",
            })

    return analyse_spending
