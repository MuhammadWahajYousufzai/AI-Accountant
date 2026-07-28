from collections import defaultdict

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.transaction_repo import TransactionRepository
from app.repositories.account_repo import AccountRepository
from app.repositories.category_repo import CategoryRepository


async def generate_profit_loss(db: AsyncSession, user_id: str, date_from: str, date_to: str):
    repo = TransactionRepository(db)
    txns = await repo.get_range(user_id, date_from, date_to)

    total_income = 0
    total_expense = 0
    income_by_cat = defaultdict(int)
    expense_by_cat = defaultdict(int)

    cat_repo = CategoryRepository(db)
    categories = await cat_repo.list(user_id)
    cat_map = {c.id: c.name for c in categories}

    for txn in txns:
        cat_name = cat_map.get(txn.category_id, "Uncategorized")
        if txn.type == "income":
            total_income += txn.amount_cents
            income_by_cat[cat_name] += txn.amount_cents
        else:
            total_expense += txn.amount_cents
            expense_by_cat[cat_name] += txn.amount_cents

    def make_breakdown(data, total):
        return [
            {"category": name, "amount_cents": amount, "percentage": round(amount / total * 100, 1) if total else 0}
            for name, amount in sorted(data.items(), key=lambda x: -x[1])
        ]

    net = total_income - total_expense

    return {
        "period": {"from": date_from, "to": date_to},
        "total_income_cents": total_income,
        "total_expense_cents": total_expense,
        "net_profit_cents": net,
        "currency": "GBP",
        "expense_breakdown": make_breakdown(expense_by_cat, total_expense),
        "income_breakdown": make_breakdown(income_by_cat, total_income),
    }


async def generate_balance_sheet(db: AsyncSession, user_id: str, as_of_date: str):
    repo = TransactionRepository(db)
    acc_repo = AccountRepository(db)

    all_txns = await repo.get_range(user_id, "1970-01-01", as_of_date)
    accounts = await acc_repo.list(user_id)
    acc_map = {a.id: a for a in accounts}

    balances: dict[str, int] = defaultdict(int)
    for txn in all_txns:
        if txn.account_id:
            acc = acc_map.get(txn.account_id)
            if acc:
                if acc.type in ("asset", "expense"):
                    if txn.type == "expense":
                        balances[txn.account_id] += txn.amount_cents
                    elif txn.type == "income":
                        balances[txn.account_id] -= txn.amount_cents
                else:
                    if txn.type == "income":
                        balances[txn.account_id] += txn.amount_cents
                    elif txn.type == "expense":
                        balances[txn.account_id] -= txn.amount_cents

    assets = []
    liabilities = []
    equity = []
    total_assets = 0
    total_liabilities = 0
    total_equity = 0

    for acc_id, balance in balances.items():
        acc = acc_map.get(acc_id)
        if not acc:
            continue
        item = {"account": acc.name, "amount_cents": balance}
        if acc.type == "asset":
            assets.append(item)
            total_assets += balance
        elif acc.type == "liability":
            liabilities.append(item)
            total_liabilities += balance
        elif acc.type == "equity":
            equity.append(item)
            total_equity += balance

    return {
        "as_of_date": as_of_date,
        "total_assets_cents": total_assets,
        "total_liabilities_cents": total_liabilities,
        "total_equity_cents": total_equity,
        "assets": assets,
        "liabilities": liabilities,
        "equity": equity,
    }


async def get_dashboard_summary(db: AsyncSession, user_id: str, month: str | None = None):
    repo = TransactionRepository(db)
    all_txns = await repo.get_all(user_id)

    if not all_txns:
        return {
            "total_income_cents": 0,
            "total_expense_cents": 0,
            "net_profit_cents": 0,
            "cash_position_cents": 0,
            "monthly_income": [],
            "monthly_expenses": [],
            "recent_transactions": [],
            "category_breakdown": [],
            "ai_insights": "No data available yet. Start by adding expenses and income.",
        }

    total_income = sum(t.amount_cents for t in all_txns if t.type == "income")
    total_expense = sum(t.amount_cents for t in all_txns if t.type == "expense")

    monthly_income_map = defaultdict(int)
    monthly_expense_map = defaultdict(int)
    for t in all_txns:
        key = str(t.date)[:7]
        if t.type == "income":
            monthly_income_map[key] += t.amount_cents
        else:
            monthly_expense_map[key] += t.amount_cents

    monthly_income = [{"month": k, "amount_cents": v} for k, v in sorted(monthly_income_map.items())]
    monthly_expenses = [{"month": k, "amount_cents": v} for k, v in sorted(monthly_expense_map.items())]

    recent = sorted(all_txns, key=lambda t: t.created_at, reverse=True)[:5]
    recent_txns = [
        {
            "id": t.id,
            "type": t.type,
            "amount_cents": t.amount_cents,
            "description": t.description,
            "date": str(t.date),
        }
        for t in recent
    ]

    cat_repo = CategoryRepository(db)
    cats = await cat_repo.list(user_id)
    cat_map = {c.id: c.name for c in cats}
    cat_expense = defaultdict(int)
    for t in all_txns:
        if t.type == "expense" and t.category_id:
            cat_expense[t.category_id] += t.amount_cents

    total_cat = sum(cat_expense.values())
    cat_breakdown = [
        {"category": cat_map.get(cid, "Other"), "amount_cents": amt, "percentage": round(amt / total_cat * 100, 1) if total_cat else 0}
        for cid, amt in sorted(cat_expense.items(), key=lambda x: -x[1])
    ]

    cash_balance = total_income - total_expense
    insights = _generate_insights(total_income, total_expense, total_cat, cat_expense, cat_map)

    return {
        "total_income_cents": total_income,
        "total_expense_cents": total_expense,
        "net_profit_cents": total_income - total_expense,
        "cash_position_cents": cash_balance,
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "recent_transactions": recent_txns,
        "category_breakdown": cat_breakdown,
        "ai_insights": insights,
    }


def _generate_insights(total_income, total_expense, total_cat, cat_expense, cat_map):
    parts = []
    if total_income > 0 and total_expense > 0:
        ratio = total_expense / total_income * 100
        if ratio > 90:
            parts.append(f"Your expense-to-income ratio is {ratio:.0f}%, which is quite high.")
        elif ratio > 70:
            parts.append(f"Your expense-to-income ratio is {ratio:.0f}%, which is moderate.")
        else:
            parts.append(f"Your expense-to-income ratio is {ratio:.0f}%, which is healthy.")

    if cat_expense:
        top_cat_id = max(cat_expense, key=cat_expense.get)
        top_name = cat_map.get(top_cat_id, "Other")
        parts.append(f"Your highest expense category is '{top_name}'.")

    return " ".join(parts) if parts else "Your financial data looks clean."
