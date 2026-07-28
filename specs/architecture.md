# Architecture Document

## 1. System Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│              Next.js + TypeScript + Tailwind                  │
│         App Router │ Dashboard │ AI Chat UI                  │
└──────────────────────┬───────────────────────────────────────┘
                       │ HTTPS / REST (JSON)
┌──────────────────────▼───────────────────────────────────────┐
│                    Backend (FastAPI)                          │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌────────┐  ┌──────────────┐   │
│  │ Auth API │  │Expense/  │  │ Reports│  │   AI Chat    │   │
│  │ /api/v1/ │  │Income API│  │ API   │  │  /api/v1/ai  │   │
│  │   auth   │  │/api/v1/  │  │/api/v1 │  └──────┬───────┘   │
│  └──────────┘  │expense   │  │/reports│         │           │
│                │income    │  └────────┘         │           │
│                │transactions│                   │           │
│                └──────────┘                     │           │
│  ┌──────────────────────────────────────────────▼────────┐   │
│  │           AI Agent Layer (OpenAI Agents SDK)           │   │
│  │                                                       │   │
│  │  ┌────────────────────────────────────────────────┐   │   │
│  │  │            Triage Agent (Router)               │   │   │
│  │  └──────┬──────────────┬──────────────┬───────────┘   │   │
│  │    ┌────▼────┐   ┌─────▼─────┐   ┌───▼──────────┐    │   │
│  │    │ Expense │   │  Income   │   │ Report/Audit │    │   │
│  │    │ Agent   │   │  Agent    │   │   Agent      │    │   │
│  │    └────┬────┘   └─────┬─────┘   └───┬──────────┘    │   │
│  │         │              │             │               │   │
│  │    ┌────▼──────────────▼─────────────▼───────────┐   │   │
│  │    │           Controlled Tool Layer              │   │   │
│  │    │  (each tool prunes output before return)     │   │   │
│  │    └──────────────────────────────────────────────┘   │   │
│  └───────────────────────────────────────────────────────┘   │
│                       │                                       │
│              ┌────────▼────────┐                              │
│              │  Service Layer  │                              │
│              │ (SQLAlchemy 2.x)│                              │
│              └────────┬────────┘                              │
└───────────────────────┬───────────────────────────────────────┘
                        │
┌───────────────────────▼───────────────────────────────────────┐
│                    PostgreSQL                                  │
│  users │ accounts │ categories │ transactions                 │
│  journal_entries │ ledger_entries │ audit_runs                  │
│  ai_conversations │ ai_messages                               │
└───────────────────────────────────────────────────────────────┘
```

## 2. Frontend Architecture

### 2.1 Stack
- Next.js 14+ with App Router
- TypeScript (strict mode)
- Tailwind CSS for styling
- Reusable component library (shadcn/ui patterns)

### 2.2 Route Structure
```
/app
  /(auth)           - Auth pages (login, register)
    /login
    /register
  /(dashboard)      - Protected dashboard routes
    /dashboard      - Main dashboard
    /expenses       - Expense management
    /income         - Income management
    /reports        - Reports (P&L, Balance Sheet)
    /audit          - Monthly audit
    /ai             - AI chat interface
  /layout.tsx       - Root layout with auth check
  /providers.tsx    - Context providers (auth, theme)
```

### 2.3 Component Architecture
```
/components
  /ui               - Base UI (button, input, card, table, etc.)
  /layout           - Sidebar, header, page shell
  /dashboard        - Dashboard widgets
  /expenses         - Expense form, list, filters
  /income           - Income form, list, filters
  /reports          - P&L and balance sheet views
  /audit            - Audit results display
  /ai-chat          - Chat UI, message components
  /charts           - Reusable chart components (recharts)
```

### 2.4 State Management
- Server state: React Query (TanStack Query) for API calls
- Auth state: React Context + JWT token in localStorage
- Form state: React Hook Form + Zod validation

### 2.5 API Integration Layer
```
/lib
  /api-client.ts    - Axios/fetch wrapper with auth headers
  /api/auth.ts      - Auth API functions
  /api/expenses.ts  - Expense API functions
  /api/income.ts    - Income API functions
  /api/reports.ts   - Report API functions
  /api/ai.ts        - AI chat API functions
/types
  /api.ts           - API request/response TypeScript types
  /models.ts        - Domain model types
```

## 3. Backend Architecture

### 3.1 Stack
- Python 3.12+
- FastAPI with async support
- SQLAlchemy 2.x (async)
- Alembic for migrations
- Pydantic v2 for validation
- OpenAI Agents SDK for AI orchestration

### 3.2 Project Structure
```
backend/
  app/
    api/
      v1/
        __init__.py
        auth.py       - /api/v1/auth
        expenses.py   - /api/v1/expenses
        income.py     - /api/v1/income
        transactions.py - /api/v1/transactions
        accounts.py   - /api/v1/accounts
        reports.py    - /api/v1/reports
        audit.py      - /api/v1/audit
        ai.py         - /api/v1/ai
    core/
      __init__.py
      config.py       - Settings from env vars
      database.py     - SQLAlchemy engine, session
      security.py     - JWT, password hashing
      deps.py         - FastAPI dependencies
    models/
      __init__.py
      user.py
      account.py
      category.py
      transaction.py
      journal_entry.py
      ledger_entry.py
      audit.py
      ai_conversation.py
    schemas/
      __init__.py
      auth.py
      expense.py
      income.py
      transaction.py
      account.py
      category.py
      report.py
      audit.py
      ai.py
    services/
      __init__.py
      auth_service.py
      expense_service.py
      income_service.py
      transaction_service.py
      account_service.py
      report_service.py
      audit_service.py
    repositories/
      __init__.py
      base.py
      expense_repo.py
      income_repo.py
      transaction_repo.py
      account_repo.py
      category_repo.py
    agents/
      __init__.py
      triage_agent.py
      expense_agent.py
      income_agent.py
      report_agent.py
      audit_agent.py
      agent_factory.py
    tools/
      __init__.py
      expense_tools.py
      income_tools.py
      transaction_tools.py
      report_tools.py
      audit_tools.py
    reports/
      __init__.py
      profit_loss.py
      balance_sheet.py
    main.py           - FastAPI app entry point
  migrations/
    versions/
  pyproject.toml
```

### 3.3 Layer Responsibilities

**API Layer** (`api/v1/`)
- Route definitions and HTTP handling
- Request validation via Pydantic schemas
- Response serialization
- Authentication dependency injection

**Service Layer** (`services/`)
- Business logic
- Accounting calculations
- Orchestrating repository calls
- Transaction management

**Repository Layer** (`repositories/`)
- Database access via SQLAlchemy
- Query building
- Data access abstraction

**Agent Layer** (`agents/`)
- OpenAI Agents SDK configuration
- Agent definitions and handoffs
- Tool registration
- Prompt management

**Tool Layer** (`tools/`)
- Controlled function tools for the AI agent
- Each tool performs validation before calling services
- Tool output is pruned to minimum before returning to LLM

## 4. Authentication Flow

```
User → Login Form → POST /api/v1/auth/login
  → Validate email/password
  → Verify password hash (bcrypt)
  → Generate JWT (24h expiry)
  → Return { access_token, token_type, user }

Protected Route → Check Authorization header
  → Verify JWT signature
  → Extract user_id from payload
  → Inject current_user dependency
  → Route handler executes with user context
```

## 5. AI Agent Flow

```
User Message → POST /api/v1/ai/chat
  → Create/reuse conversation
  → Append user message to history
  → Triage Agent (OpenAI Agents SDK)
    → Determine intent (expense, income, report, audit, query)
    → Handoff to specialist agent
      → Specialist calls controlled tool
        → Tool validates args via Pydantic
        → Tool calls service layer
        → Service layer queries/writes to PostgreSQL
        → Tool prunes output to minimum fields
        → Return result to agent
      → Agent generates natural language response
    → Append assistant message to history
  → Return response to frontend
```

## 6. Security Architecture

- **Password Hashing**: bcrypt (via passlib)
- **JWT**: RS256 or HS256 with 24h access token
- **API Protection**: every route except auth requires valid JWT
- **Data Isolation**: all queries include `user_id = current_user.id`
- **CORS**: restricted to frontend origin
- **Environment**: secrets via `.env`, never in code
- **AI Safety**: no arbitrary SQL, only controlled tool calls, delete requires confirmation

## 7. Error Handling Strategy

- Consistent error response format: `{ detail: string, code: string }`
- HTTP status codes follow REST conventions
- Service layer raises typed exceptions
- API layer catches and returns appropriate HTTP responses
- AI agent errors are caught and returned as user-friendly messages
- Unhandled exceptions return 500 with generic message (details logged)
