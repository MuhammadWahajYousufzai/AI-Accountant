import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(10), nullable=False)
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="GBP")
    description: Mapped[str] = mapped_column(Text, nullable=False)
    vendor_source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    date: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    category_id: Mapped[str | None] = mapped_column(String, ForeignKey("categories.id"), nullable=True)
    account_id: Mapped[str | None] = mapped_column(String, ForeignKey("accounts.id"), nullable=True)
    is_reconciled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="transactions")
