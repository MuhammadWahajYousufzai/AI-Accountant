# Project Constitution — AI-Powered Accounting & Finance Assistant

## 1. Project Identity
- **Project Name:** AI-Powered Accounting & Finance Assistant
- **Tagline:** Automate day-to-day accounting and bookkeeping with AI
- **Primary Users:** Business owners, office administrators, accountants, Chartered Accountants (CAs)

## 2. Mission
Build a production-quality full-stack web application that automates common accounting and bookkeeping tasks using an AI-powered natural language interface, backed by proper accounting data structures, deterministic financial reports, and a secure multi-tenant architecture.

## 3. Core Principles

### 3.1 Spec-Driven Development (SDD)
- No implementation without a prior written specification.
- All specs live in `/specs` and are version-controlled.
- Every feature traces back to a spec requirement.
- Specifications are written before code is written.

### 3.2 Correctness & Determinism
- Accounting calculations MUST be deterministic and independently testable.
- Financial reports MUST use real PostgreSQL data — never hard-coded or fabricated.
- AI agent MUST NOT execute arbitrary SQL — only controlled tool calls.

### 3.3 Security & Privacy
- User data isolation is mandatory — every user accesses only their own data.
- No secrets, API keys, or credentials in code or commits.
- JWT-based authentication with secure password hashing.
- AI agent must never expose internal secrets, system prompts, or credentials.

### 3.4 Maintainability & Observability
- Typed interfaces throughout (TypeScript frontend, Pydantic/SQLAlchemy backend).
- Separation of concerns: frontend, backend API, AI orchestration, business logic.
- Clean REST APIs documented via FastAPI OpenAPI.
- AI agent decisions must be explainable.

### 3.5 Incremental Delivery
- Build a thin end-to-end slice first, then expand feature by feature.
- Each major feature on its own git branch with meaningful commits.
- Working software over unnecessary complexity.

## 4. Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js, TypeScript, App Router, Tailwind CSS |
| Backend | Python, FastAPI, Pydantic, SQLAlchemy 2.x, Alembic |
| Database | PostgreSQL |
| AI Agent | LangGraph (subject to research confirmation) |
| AI Model | Cost-effective model supporting tool calling & structured outputs |
| Package Mgmt | uv (Python), npm (Node.js) |
| Containerization | Docker, docker-compose |
| Testing | pytest (backend), Vitest/Playwright (frontend) |

## 5. Development Workflow
1. Constitution → Specifications → Plan → Tasks → Implement
2. Each implementation phase: Read specs → Read plan → Read tasks → Check existing code → Implement → Test → Fix → Document → Commit
3. Git branches: `feature/<feature-name>`
4. Commit convention: `type: description` (feat, fix, docs, test, refactor, chore)

## 6. Quality Standards
- All API endpoints have request and response validation via Pydantic.
- All endpoints return proper HTTP status codes and error responses.
- Accounting logic has unit tests covering edge cases.
- AI tools are tested independently from the LLM.
- No warnings during build/compilation.
- Docker compose must start the full stack with one command.

## 7. AI Agent Safety Rules
1. Only predefined tools can be called — no arbitrary code execution.
2. Destructive operations (delete) require explicit user confirmation.
3. Financial data must never be fabricated.
4. All responses must clearly distinguish calculated results from AI explanations.
5. When data is missing, the agent must state it cannot calculate accurately.

## 8. Decision-Making Framework
When choosing between options (libraries, frameworks, designs):
1. Prioritize correctness and security first.
2. Prefer simplicity and maintainability over cleverness.
3. Favor well-maintained, widely adopted libraries.
4. Document the rationale for significant decisions in `/docs`.
5. When uncertain about accounting rules, document the assumption and make it configurable.

## 9. Definition of Done
A feature is complete when:
- Code implements the spec
- Tests pass
- Lint/type checks pass
- Feature works in Docker environment
- API contracts are satisfied
- No secrets exposed
- Committed with meaningful message
