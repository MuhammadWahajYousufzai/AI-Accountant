# AI-Powered Accounting & Finance Assistant

A full-stack web application that automates day-to-day accounting and bookkeeping tasks using an AI-powered natural language interface.

## Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Backend**: Python 3.12+, FastAPI, SQLAlchemy 2.x, Alembic
- **Database**: PostgreSQL
- **AI Agent**: OpenAI Agents SDK (with Gemini via OpenAI-compatible API)
- **AI Model**: Gemini 2.0 Flash (configurable via env var)
- **Containerization**: Docker, docker-compose

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Google Gemini API key (for AI features)

### Running with Docker

```bash
# Clone and enter the project
git clone <repo-url> && cd AI-Powered-Accounting-Finance-Assistant

# Copy environment file and add your OpenAI API key
cp .env.example .env
# Edit .env and set GOOGLE_API_KEY

# Start everything
docker compose up --build
```

The app will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Running without Docker

**Backend:**
```bash
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Database:**
```bash
docker run -d --name accounting-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=accounting -p 5432:5432 postgres:16-alpine
```

## Features

- **Authentication** — Registration, login, JWT-based auth, protected routes
- **Dashboard** — Income, expenses, net profit, cash position, charts, AI insights
- **Expense Management** — CRUD, search, filter by category/date/amount
- **Income Management** — CRUD, search, filter by source/date
- **Profit & Loss** — Period-based reports with category breakdowns
- **Balance Sheet** — Assets, liabilities, equity from real accounting data
- **Monthly Audit** — Duplicate detection, anomaly detection, categorization review
- **AI Assistant** — Natural language interface for all accounting operations
- **Spending Analysis** — Category trends, pattern detection, comparisons

## AI Agent Capabilities

The AI assistant can:
- Create expenses and income from natural language
- Query and search transactions
- Generate P&L and balance sheet reports
- Run monthly audits with anomaly detection
- Analyse spending patterns
- Summarise financial activity
- Answer date-specific financial questions

## Project Structure

```
├── frontend/         # Next.js application
│   ├── app/          # App Router pages
│   ├── components/   # Reusable UI components
│   ├── lib/          # API client, auth context
│   └── types/        # TypeScript type definitions
├── backend/
│   ├── app/
│   │   ├── api/v1/   # REST API routes
│   │   ├── core/     # Config, database, security
│   │   ├── models/   # SQLAlchemy models
│   │   ├── schemas/  # Pydantic validation schemas
│   │   ├── services/ # Business logic
│   │   ├── repositories/ # Data access layer
│   │   ├── agents/   # OpenAI Agents SDK agents
│   │   └── tools/    # Controlled AI tools
│   ├── migrations/   # Alembic migrations
│   └── pyproject.toml
├── specs/            # All specifications
├── docs/             # Research and architecture docs
├── tests/            # Backend tests
└── docker-compose.yml
```

## Spec-Driven Development

All specifications are in `/specs`:
- `constitution.md` — Project governing principles
- `product-requirements.md` — Functional and non-functional requirements
- `architecture.md` — System architecture
- `database-schema.md` — Database design
- `api-contracts.md` — API request/response schemas
- `ai-agent-spec.md` — AI agent architecture and tools
- `implementation-plan.md` — Build plan and task breakdown

Research and design docs are in `/docs`.
