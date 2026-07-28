from collections import defaultdict
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditRun, AuditFinding
from app.repositories.transaction_repo import TransactionRepository
from app.repositories.category_repo import CategoryRepository


async def run_audit(db: AsyncSession, user_id: str, period_start: str, period_end: str):
    repo = TransactionRepository(db)
    txns = await repo.get_range(user_id, period_start, period_end)

    audit_run = AuditRun(
        user_id=user_id,
        period_start=period_start,
        period_end=period_end,
        status="completed",
    )
    db.add(audit_run)
    await db.flush()

    findings = []

    findings.extend(_check_duplicates(txns, audit_run.id))
    findings.extend(_check_missing_info(txns, audit_run.id))
    findings.extend(_check_unusual_amounts(txns, audit_run.id))
    findings.extend(_check_categorization(txns, audit_run.id))
    findings.extend(_check_date_inconsistencies(txns, audit_run.id, period_start, period_end))

    for f in findings:
        db.add(f)

    summary = f"Audit found {len(findings)} issue(s)."
    if findings:
        severity_counts = defaultdict(int)
        for f in findings:
            severity_counts[f.severity] += 1
        parts = []
        for sev in ("high", "medium", "low"):
            if severity_counts[sev]:
                parts.append(f"{severity_counts[sev]} {sev}")
        summary = f"Audit found {len(findings)} issue(s): {', '.join(parts)}."

    audit_run.summary = summary
    await db.flush()

    return {
        "id": audit_run.id,
        "period": {"start": period_start, "end": period_end},
        "status": "completed",
        "findings": [
            {
                "type": f.finding_type,
                "severity": f.severity,
                "transaction_id": f.transaction_id,
                "description": f.description,
            }
            for f in findings
        ],
        "summary": summary,
        "disclaimer": "This is an AI-assisted audit and does not replace professional audit or legal/tax advice.",
    }


def _check_duplicates(txns, audit_run_id):
    findings = []
    seen = defaultdict(list)

    for t in txns:
        key = (abs(t.amount_cents), t.vendor_source)
        seen[key].append(t)

    for key, group in seen.items():
        if len(group) > 1:
            for t in group[1:]:
                findings.append(
                    AuditFinding(
                        audit_run_id=audit_run_id,
                        finding_type="duplicate",
                        severity="high",
                        transaction_id=t.id,
                        description=f"Possible duplicate: {len(group)} transactions of {_fmt_cents(key[0])} from '{key[1] or 'unknown'}'.",
                    )
                )
    return findings


def _check_missing_info(txns, audit_run_id):
    findings = []
    for t in txns:
        missing = []
        if not t.description or t.description.strip() == "":
            missing.append("description")
        if not t.vendor_source:
            missing.append("vendor/source")
        if not t.category_id:
            missing.append("category")

        if missing:
            findings.append(
                AuditFinding(
                    audit_run_id=audit_run_id,
                    finding_type="missing_info",
                    severity="medium",
                    transaction_id=t.id,
                    description=f"Missing information: {', '.join(missing)}.",
                )
            )
    return findings


def _check_unusual_amounts(txns, audit_run_id):
    findings = []
    amounts = [t.amount_cents for t in txns]
    if not amounts:
        return findings

    mean = sum(amounts) / len(amounts)
    std = (sum((a - mean) ** 2 for a in amounts) / len(amounts)) ** 0.5

    if std > 0:
        for t in txns:
            if t.amount_cents > mean + 2.5 * std:
                findings.append(
                    AuditFinding(
                        audit_run_id=audit_run_id,
                        finding_type="unusual_amount",
                        severity="medium",
                        transaction_id=t.id,
                        description=f"Unusual amount: {_fmt_cents(t.amount_cents)} is significantly above the average of {_fmt_cents(int(mean))}.",
                    )
                )
    return findings


def _check_categorization(txns, audit_run_id):
    findings = []
    for t in txns:
        if not t.category_id and t.amount_cents > 10000:
            findings.append(
                AuditFinding(
                    audit_run_id=audit_run_id,
                    finding_type="categorization_issue",
                    severity="low",
                    transaction_id=t.id,
                    description=f"Large transaction ({_fmt_cents(t.amount_cents)}) without a category assigned.",
                )
            )
    return findings


def _check_date_inconsistencies(txns, audit_run_id, period_start, period_end):
    findings = []
    ps = datetime.strptime(period_start, "%Y-%m-%d").date()
    pe = datetime.strptime(period_end, "%Y-%m-%d").date()

    for t in txns:
        if hasattr(t.date, "strftime"):
            txn_date = t.date
        else:
            txn_date = datetime.strptime(str(t.date), "%Y-%m-%d").date()

        if txn_date < ps or txn_date > pe:
            findings.append(
                AuditFinding(
                    audit_run_id=audit_run_id,
                    finding_type="date_inconsistency",
                    severity="medium",
                    transaction_id=t.id,
                    description=f"Transaction date {txn_date} is outside the audit period.",
                )
            )
    return findings


def _fmt_cents(cents: int) -> str:
    return f"£{cents / 100:,.2f}"
