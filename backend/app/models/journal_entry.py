import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False, index=True)
    transaction_id: Mapped[str | None] = mapped_column(String, ForeignKey("transactions.id"), nullable=True)
    entry_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    ledger_entries = relationship("LedgerEntry", back_populates="journal_entry", lazy="selectin")
