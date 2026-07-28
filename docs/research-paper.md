# Research Paper — AI-Powered Accounting & Finance Assistant

## 1. Core Accounting Responsibilities

### 1.1 Daily Tasks
- Recording financial transactions (sales, purchases, receipts, payments)
- Bank reconciliation — matching bank statements against ledgers
- Managing accounts payable and receivable
- Categorizing expenses and income
- Maintaining the general ledger

### 1.2 Monthly Tasks
- Preparing management accounts
- Reconciling all bank and credit card accounts
- Running profit & loss statements
- Reviewing balance sheet
- VAT/sales tax returns
- Following up on missing receipts and invoices
- Anomaly detection and investigation

### 1.3 Yearly Tasks
- Year-end accounts preparation
- Tax return preparation and filing
- Audit preparation and support
- Fixed asset registers and depreciation
- Financial statement finalization
- Budget vs actual analysis

## 2. Tasks Suitable for AI Automation

| Task | Automation Potential | Complexity | AI Approach |
|------|-------------------|------------|-------------|
| Transaction categorization | High (>95%) | Low | Pattern recognition from historical data |
| Expense data entry | High | Low | NLU from natural language descriptions |
| Bank reconciliation | High | Medium | Rule-based matching + ML confidence scoring |
| P&L generation | High | Low | Deterministic calculation from ledger |
| Balance sheet generation | High | Low | Deterministic calculation from ledger |
| Monthly audit checks | Medium-High | Medium | Rule-based checks + anomaly detection |
| Financial summarization | High | Medium | LLM summarization of structured data |
| Duplicate detection | High | Low | Fuzzy matching on transaction attributes |
| Spending analysis | High | Medium | Aggregation + trend analysis |
| Cash flow reporting | Medium | Medium | Aggregation of income/expense timing |

### 2.1 Tasks NOT Suitable for Full Automation
- Final sign-off on financial statements
- Complex tax position judgment
- Fraud investigation requiring human judgment
- Strategic financial advice
- Regulatory filing (requires licensed professional)

## 3. Agentic AI Architecture

Agentic AI refers to systems where an AI model can:
1. **Perceive** — receive natural language or structured input
2. **Reason** — determine intent and plan steps
3. **Act** — call controlled tools/functions to affect the system
4. **Observe** — read results and adjust
5. **Iterate** — continue until the task is complete or handoff is needed

For accounting, this means the AI can understand "Record office rent of £50,000 for July" and execute the full workflow: validate → check for duplicates → create transaction → post to ledger → confirm.

### 3.1 Key Architecture Decisions
- **Tool-based access** — AI never executes arbitrary SQL; only calls predefined tools
- **Confidence thresholds** — low-confidence actions are queued for human review
- **Audit trail** — every AI action is logged with reasoning
- **User isolation** — AI operates within the authenticated user's data scope
- **Deterministic reports** — P&L, balance sheet are computed, not LLM-generated

## 4. Agentic Framework Comparison

### 4.1 LangGraph
| Aspect | Assessment |
|--------|-----------|
| Architecture | Directed state graphs with typed state, nodes, and conditional edges |
| Model Support | 100+ models (model-agnostic) |
| State Persistence | Built-in checkpointing (SQLite, PostgreSQL out of the box) |
| Human-in-the-Loop | Native interrupt/resume |
| Observability | LangSmith integration — full execution traces, time-travel debugging |
| Learning Curve | 1-2 weeks |
| Production Readiness | High — used by Klarna, Uber, LinkedIn, Elastic |
| Cost Efficiency | Lowest token overhead (~5%) due to explicit graph control |
| Complex Task Success | 62% |
| License | MIT |
| GitHub Stars | ~27K |
| PyPI Downloads | 39.2M/month |

### 4.2 CrewAI
| Aspect | Assessment |
|--------|-----------|
| Architecture | Role-based agent teams with declarative tasks |
| Model Support | 100+ models (model-agnostic) |
| State Persistence | Session memory only |
| Human-in-the-Loop | Via callbacks |
| Observability | Built-in logging, third-party support |
| Learning Curve | Hours to days |
| Production Readiness | Medium-High |
| Cost Efficiency | ~18% token overhead from role/backstory prompts |
| Complex Task Success | 54% |
| License | MIT |
| GitHub Stars | ~46K |

### 4.3 OpenAI Agents SDK
| Aspect | Assessment |
|--------|-----------|
| Architecture | Agents + handoffs + guardrails (minimal primitives) |
| Model Support | OpenAI only (100+ via LiteLLM beta) |
| State Persistence | Manual implementation required |
| Human-in-the-Loop | Manual implementation |
| Observability | OpenAI tracing |
| Learning Curve | Hours |
| Production Readiness | Medium (pre-1.0, v0.10.2) |
| Cost Efficiency | ~8% token overhead |
| Complex Task Success | ~50% |
| License | MIT |
| GitHub Stars | ~20K |

### 4.4 Selected Framework: OpenAI Agents SDK

**Justification:**
1. **Simplicity and speed to production** — Minimal API surface (agents, handoffs, guardrails) means faster development and fewer concepts to learn. Working agents in hours, not weeks.
2. **Built-in guardrails** — Native input/output tripwire validation provides production-ready safety out of the box, essential for accounting operations.
3. **First-party tracing** — Built-in observability with visualization and debugging tools via OpenAI platform, giving visibility into every agent decision.
4. **Model flexibility in 2026** — The SDK now supports 100+ non-OpenAI models via documented integration paths, removing vendor lock-in concerns.
5. **Handoff pattern** — Natural fit for accounting workflows where a triage agent routes to specialist agents (expenses, reports, audit).
6. **Pre-1.0 but rapidly maturing** — Active development with strong community adoption. For our focused single-purpose accounting agents, the SDK's capabilities are sufficient without the overhead of a graph framework.
7. **Cost efficiency** — ~8% token overhead with built-in tracing, compared to ~18% for CrewAI. No additional infrastructure costs for state persistence (we handle this at the application layer).

## 5. AI Model Selection

### 5.1 Requirements
- Tool/function calling support
- Structured output (JSON mode)
- Natural language understanding for accounting queries
- Cost-effectiveness for startup deployment
- Reasonable latency (<5s end-to-end)

### 5.2 Shortlisted Models

| Model | Tool Calling | Structured Output | Cost (per 1M tokens) | Latency | Notes |
|-------|-------------|-------------------|---------------------|---------|-------|
| GPT-4o-mini | Excellent | Excellent | $0.15/$0.60 | Fast | Best balance of cost/capability |
| Claude 3.5 Haiku | Excellent | Excellent | $0.25/$1.25 | Fast | Strong at structured extraction |
| Gemini 1.5 Flash | Good | Good | $0.075/$0.30 | Fastest | Cheapest, context caching |
| DeepSeek-V3 | Good | Good | $0.27/$1.10 | Moderate | Open-weight alternative |

### 5.3 Selected Default Model: GPT-4o-mini
- Best cost-to-capability ratio for structured accounting tasks
- Strong tool-calling reliability
- Fast inference speed for interactive chat
- Wide ecosystem support

The architecture uses a **provider abstraction layer** so the model can be swapped via environment variable without code changes.

## 6. System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                        Frontend                          │
│              Next.js + TypeScript + Tailwind              │
│         App Router │ Dashboard │ AI Chat UI              │
└──────────────────────┬───────────────────────────────────┘
                       │ HTTPS / REST
┌──────────────────────▼───────────────────────────────────┐
│                    Backend (FastAPI)                      │
│  ┌──────────┐ ┌──────────┐ ┌────────┐ ┌──────────────┐  │
│  │ Auth API │ │Expense/  │ │ Reports│ │   AI Chat    │  │
│  │ /api/v1/ │ │Income API│ │ API   │ │   /api/v1/ai │  │
│  │   auth   │ │/api/v1/  │ │/api/v1 │ └──────┬───────┘  │
│  └──────────┘ │expense   │ │/reports│        │          │
│               │income    │ └────────┘        │          │
│               └──────────┘                   │          │
│  ┌────────────────────────────────────────────▼──────┐   │
│  │           AI Agent (OpenAI Agents SDK)            │   │
│  │  ┌────────────────────────────────────────────┐   │   │
│  │  │           Triage Agent                     │   │   │
│  │  │  (routes intent via handoffs)              │   │   │
│  │  └────┬──────────┬──────────┬─────────────────┘   │   │
│  │  ┌────▼──┐ ┌─────▼─────┐ ┌─▼──────────────┐      │   │
│  │  │Expense│ │  Income   │ │  Report/Audit  │      │   │
│  │  │Agent  │ │  Agent    │ │    Agent       │      │   │
│  │  └───┬───┘ └─────┬─────┘ └───┬───────────┘      │   │
│  │      │           │           │                    │   │
│  │  ┌───▼───────────▼───────────▼────────────────┐   │   │
│  │  │         Tool Layer (controlled)             │   │   │
│  │  │  create_expense │ create_income             │   │   │
│  │  │  list_expenses  │ search_transactions       │   │   │
│  │  │  generate_pl    │ generate_balance_sheet    │   │   │
│  │  │  run_audit      │ get_financial_summary     │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └────────────────────────────────────────────────────┘   │
│                       │                                    │
│              ┌────────▼────────┐                          │
│              │ Service Layer   │                          │
│              │ (SQLAlchemy)    │                          │
│              └────────┬────────┘                          │
└───────────────────────┬───────────────────────────────────┘
                        │
┌───────────────────────▼───────────────────────────────────┐
│                    PostgreSQL                              │
│  users │ accounts │ categories │ transactions             │
│  journal_entries │ ledger_entries │ audit_runs             │
│  ai_conversations │ ai_messages                           │
└───────────────────────────────────────────────────────────┘
```

## 7. Feature List Derived from Research

1. **Authentication** — registration, login, JWT, password hashing, protected routes
2. **Dashboard** — income/expense/net summary, monthly trends, category breakdown, AI insights
3. **Expense Management** — CRUD, search, filter, date range, categories
4. **Income Management** — CRUD, search, filter, date range, income sources
5. **Transaction Ledger** — unified view of all financial entries with journal/ledger support
6. **Profit & Loss Statement** — period-based, real data, with breakdowns
7. **Balance Sheet** — assets, liabilities, equity from accounting data
8. **Monthly Audit** — anomaly detection, duplicate check, categorization review
9. **AI Agent** — OpenAI Agents SDK-powered with controlled tools
10. **AI Chat UI** — conversational interface with structured result display
11. **Spending Analysis** — category trends, comparisons, anomalies
12. **Financial Summarization** — natural language summaries from real data

## 8. References

- LangGraph Documentation (https://docs.langchain.com/langgraph)
- CrewAI Documentation (https://docs.crewai.com)
- OpenAI Agents SDK Documentation (https://openai.github.io/openai-agents-python)
- Deloitte (Jan 2026) — AI Adoption in Finance Organizations (63% fully deployed)
- Gartner (2026) — 90% of finance functions will deploy AI during 2026
- Blue J & CPA.com (June 2026) — 60% of tax professionals use AI weekly
- Karbon (2026) — State of AI in Accounting Research
- Intuit (July 2025) — AI agents inside QuickBooks Online
- Agentmelt Case Study (2026) — 50% bookkeeping time reduction with AI accounting agent
