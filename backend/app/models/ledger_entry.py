import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False, index=True)
    journal_entry_id: Mapped[str] = mapped_column(String, ForeignKey("journal_entries.id"), nullable=False)
    account_id: Mapped[str] = mapped_column(String, ForeignKey("accounts.id"), nullable=False)
    entry_type: Mapped[str] = mapped_column(String(4), nullable=False)
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    journal_entry = relationship("JournalEntry", back_populates="ledger_entries")
