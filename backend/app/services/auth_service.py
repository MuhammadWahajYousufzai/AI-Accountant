from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.account import Account
from app.models.category import Category
from app.core.security import hash_password, verify_password, create_access_token


DEFAULT_ACCOUNTS = [
    ("Cash", "asset"),
    ("Bank Account", "asset"),
    ("Accounts Receivable", "asset"),
    ("Accounts Payable", "liability"),
    ("Owner's Equity", "equity"),
    ("Retained Earnings", "equity"),
    ("Revenue", "income"),
    ("Other Income", "income"),
    ("Cost of Goods Sold", "expense"),
    ("Operating Expenses", "expense"),
]

DEFAULT_EXPENSE_CATEGORIES = [
    "Rent", "Utilities", "Salaries", "Office Supplies", "Software",
    "Marketing", "Travel", "Meals & Entertainment", "Professional Services",
    "Insurance", "Maintenance", "Transportation", "Communication", "Other",
]

DEFAULT_INCOME_CATEGORIES = [
    "Sales", "Services", "Consulting", "Interest", "Other",
]


async def register_user(db: AsyncSession, email: str, password: str, full_name: str) -> tuple[User, str]:
    existing = await db.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        raise ValueError("Email already registered")

    user = User(
        email=email,
        password_hash=hash_password(password),
        full_name=full_name,
    )
    db.add(user)
    await db.flush()

    for name, type_ in DEFAULT_ACCOUNTS:
        account = Account(user_id=user.id, name=name, type=type_, is_system=True)
        db.add(account)

    for name in DEFAULT_EXPENSE_CATEGORIES:
        category = Category(user_id=user.id, name=name, type="expense", is_system=True)
        db.add(category)

    for name in DEFAULT_INCOME_CATEGORIES:
        category = Category(user_id=user.id, name=name, type="income", is_system=True)
        db.add(category)

    await db.flush()

    token = create_access_token(user.id)
    return user, token


async def login_user(db: AsyncSession, email: str, password: str) -> tuple[User, str]:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid email or password")

    token = create_access_token(user.id)
    return user, token
