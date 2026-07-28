# Implementation Plan

## Phase 0: Project Setup
1. Initialize git repository
2. Create monorepo structure (`frontend/`, `backend/`)
3. Configure Python with `uv` (pyproject.toml, dependencies)
4. Initialize Next.js frontend with TypeScript + Tailwind
5. Create `.env.example` and configuration files
6. Create `.gitignore`
7. Create Docker setup (Dockerfile.frontend, Dockerfile.backend, docker-compose.yml)

## Phase 1: Backend Foundation
1. FastAPI app setup with CORS, middleware
2. PostgreSQL connection with SQLAlchemy 2.x async
3. Alembic migrations for all tables
4. Settings/config management (pydantic-settings)
5. Seed default accounts and categories

## Phase 2: Authentication
1. User model and migration
2. Password hashing service (bcrypt)
3. JWT token generation and validation
4. Auth API endpoints (register, login, me)
5. Auth dependency for protected routes
6. Seed default data on registration

## Phase 3: Core CRUD APIs
1. Category CRUD (list, create)
2. Account CRUD (list, create)
3. Expense CRUD (list, create, get, update, delete)
4. Income CRUD (list, create, get, update, delete)
5. Transaction list endpoint
6. Journal entry and ledger entry creation on expense/income

## Phase 4: Reports
1. Profit & Loss calculation service
2. Balance Sheet calculation service
3. Report API endpoints
4. Dashboard summary endpoint

## Phase 5: Audit
1. Audit service with checks:
   - Duplicate detection (same amount, vendor, similar date)
   - Missing information detection
   - Unusual amount detection (statistical outliers)
   - Spending pattern analysis
   - Categorization issue detection
2. Audit API endpoint
3. Audit findings storage

## Phase 6: AI Agent Layer
1. OpenAI Agents SDK setup
2. Tool definitions (all accounting tools)
3. Agent definitions (triage, expense, income, report, audit, query)
4. Tool output pruning implementation
5. Agent factory and provider abstraction
6. Conversation memory (from database)
7. Guardrails for safety

## Phase 7: AI Chat API
1. Conversations CRUD
2. Messages storage
3. Chat endpoint (POST /api/v1/ai/chat)
4. Streaming support (optional, future)

## Phase 8: Frontend Foundation
1. Project setup with Next.js App Router
2. Layout, sidebar, header
3. Auth pages (login, register)
4. Auth context and protected routes
5. API client setup with auth headers
6. TypeScript types for all API models

## Phase 9: Frontend Dashboard
1. Summary cards (income, expenses, net, cash)
2. Monthly chart (income vs expenses)
3. Recent transactions widget
4. Category breakdown chart
5. AI insights panel

## Phase 10: Frontend CRUD Pages
1. Expense list page with filters, pagination, search
2. Expense create/edit form
3. Income list page with filters, pagination, search
4. Income create/edit form
5. Transaction list page

## Phase 11: Frontend Reports
1. P&L report view with date picker
2. Balance sheet view with date picker
3. Report breakdown tables

## Phase 12: Frontend Audit
1. Audit run page with period selector
2. Audit findings display
3. Finding detail view

## Phase 13: AI Chat UI
1. Chat interface with message list
2. Message input
3. Tool action status indicators
4. Structured result display (tables, reports)
5. Conversation history sidebar
6. Visual distinction between message types

## Phase 14: Testing
1. Backend unit tests (services, calculations)
2. API integration tests
3. Auth tests
4. AI tool tests (deterministic, LLM-independent)
5. Frontend component tests (basic)

## Phase 15: Docker & Deployment
1. Dockerfile for frontend (multi-stage build)
2. Dockerfile for backend
3. docker-compose.yml (frontend, backend, PostgreSQL)
4. Environment configuration
5. Database migration on startup
6. README with setup instructions

## Priority Order for Implementation
1. Phase 0 (Project Setup)
2. Phase 1 (Backend Foundation)
3. Phase 2 (Authentication)
4. Phase 3 (Core CRUD APIs)
5. Phase 8 (Frontend Foundation)
6. Phase 9 (Frontend Dashboard)
7. Phase 10 (Frontend CRUD Pages)
8. Phase 4 (Reports) + Phase 11 (Frontend Reports)
9. Phase 5 (Audit) + Phase 12 (Frontend Audit)
10. Phase 6 (AI Agent) + Phase 7 (AI Chat API) + Phase 13 (AI Chat UI)
11. Phase 14 (Testing)
12. Phase 15 (Docker & Deployment)
