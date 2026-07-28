import json

from agents import function_tool


def generate_profit_loss_tool(get_db, get_user_id):
    @function_tool
    async def generate_profit_loss(date_from: str, date_to: str) -> str:
        """Generate a Profit & Loss statement for the specified date range (YYYY-MM-DD)."""
        from app.services.report_service import generate_profit_loss as svc_pl

        async with get_db() as db:
            report = await svc_pl(db, get_user_id(), date_from, date_to)
            return json.dumps(report)

    return generate_profit_loss


def generate_balance_sheet_tool(get_db, get_user_id):
    @function_tool
    async def generate_balance_sheet(as_of_date: str) -> str:
        """Generate a Balance Sheet as of the specified date (YYYY-MM-DD)."""
        from app.services.report_service import generate_balance_sheet as svc_bs

        async with get_db() as db:
            report = await svc_bs(db, get_user_id(), as_of_date)
            return json.dumps(report)

    return generate_balance_sheet


def get_financial_summary_tool(get_db, get_user_id):
    @function_tool
    async def get_financial_summary(date_from: str | None = None, date_to: str | None = None) -> str:
        """Get an aggregate financial summary. Optionally filter by date range."""
        from app.services.report_service import get_dashboard_summary

        async with get_db() as db:
            summary = await get_dashboard_summary(db, get_user_id())
            return json.dumps({
                "total_income_cents": summary["total_income_cents"],
                "total_expense_cents": summary["total_expense_cents"],
                "net_cents": summary["net_profit_cents"],
                "cash_position_cents": summary["cash_position_cents"],
            })

    return get_financial_summary
