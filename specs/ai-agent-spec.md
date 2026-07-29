# AI Agent Specification

## 1. Framework: OpenAI Agents SDK

### 1.1 Core Primitives Used
- **Agent** — LLM with instructions, tools, and handoff configuration
- **Handoffs** — delegation between specialist agents
- **Guardrails** — input/output validation for safety
- **Tracing** — built-in observability via OpenAI platform

### 1.2 Why OpenAI Agents SDK for This Project
- Minimal abstraction — easy to understand and maintain
- Handoff pattern maps naturally to accounting workflows
- Built-in guardrails for safety-critical financial operations
- First-party tracing for debugging agent behavior
- Now supports non-OpenAI models via integration paths

## 2. Agent Architecture

```
User Message
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│                  Triage Agent (Router)                   │
│  Instructions: Classify intent from user message         │
│  Tools: None (routing only via handoffs)                 │
│                                                         │
│  Handoff conditions:                                     │
│  - expense_create/list/update/delete → Expense Agent    │
│  - income_create/list/update/delete → Income Agent      │
│  - report/pl/balance_sheet → Report Agent               │
│  - audit/check/review → Audit Agent                     │
│  - general query/search/summary → Query Agent           │
│  - ambiguous → ask clarifying questions                 │
└────────┬───────────────────────────────────────────────┘
         │ handoff
    ┌────┴────┬──────────┬──────────┬───────────┐
    ▼         ▼          ▼          ▼          ▼
┌─────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌─────────┐
│ Expense │ │ Income │ │ Report │ │ Audit  │ │  Query  │
│ Agent   │ │ Agent  │ │ Agent  │ │ Agent  │ │  Agent  │
└────┬────┘ └───┬────┘ └───┬────┘ └───┬────┘ └────┬────┘
     │          │          │          │           │
     ▼          ▼          ▼          ▼           ▼
┌──────────────────────────────────────────────────────┐
│              Controlled Tool Layer                    │
│  Each tool: validates args → calls service → prunes  │
│  output before returning to LLM                      │
└──────────────────────────────────────────────────────┘
```

## 3. Agent Definitions

### 3.1 Triage Agent
```
name: "Accounting Triage Agent"
instructions: |
  You are the triage agent for an accounting system. Your job is to:
  1. Read the user's message
  2. Determine their intent
  3. Handoff to the appropriate specialist agent

  Classification rules:
  - If the user wants to CREATE, VIEW, UPDATE, or DELETE expenses → handoff to Expense Agent
  - If the user wants to CREATE, VIEW, UPDATE, or DELETE income → handoff to Income Agent
  - If the user asks for reports, P&L, balance sheet → handoff to Report Agent
  - If the user asks for audit, review, check → handoff to Audit Agent
  - If the user asks a general question or wants a summary → handoff to Query Agent
  - If unsure, ask clarifying questions

  Never refuse to handoff. Always route to the most specific agent.
handoffs: [expense_agent, income_agent, report_agent, audit_agent, query_agent]
parallel_tool_calls: false
```

### 3.2 Expense Agent
```
name: "Expense Management Agent"
instructions: |
  You are an expense management agent. You help users manage their business expenses.
  
  When creating an expense:
  - Extract: amount, description, date, category, vendor
  - Present a summary before creating if information is complete
  - Call create_expense tool to save
  
  When listing/searching: Call list_expenses with appropriate filters
  When updating: Confirm changes, call update_expense
  When deleting: ALWAYS confirm with user before deleting. Never delete on ambiguous instructions.
  
  Always use real data from the database via tools. Never fabricate numbers.
tools: [create_expense, list_expenses, get_expense, update_expense, delete_expense]
parallel_tool_calls: false
```

### 3.3 Income Agent
```
name: "Income Management Agent"
instructions: |
  You are an income management agent. You help users track their income.
  
  When creating income:
  - Extract: amount, description, date, source, category
  - Present a summary before creating
  - Call create_income tool
  
  CRUD operations follow same pattern as Expense Agent.
tools: [create_income, list_income, get_income, update_income, delete_income]
parallel_tool_calls: false
```

### 3.4 Report Agent
```
name: "Financial Report Agent"
instructions: |
  You are a financial reporting agent. You generate reports using real database data.
  
  For P&L: Ask for date range or infer from context. Call generate_profit_loss tool.
  For Balance Sheet: Ask for as-of date. Call generate_balance_sheet tool.
  For financial summary: Call get_financial_summary tool.
  
  Report calculations are done by the backend. You present the results clearly.
  Always specify the reporting period and data source in your response.
tools: [generate_profit_loss, generate_balance_sheet, get_financial_summary]
parallel_tool_calls: false
```

### 3.5 Audit Agent
```
name: "Monthly Audit Agent"
instructions: |
  You are an audit agent. You analyze transactions and identify issues.
  
  Call run_monthly_audit with the period to analyze.
  Present findings clearly, categorized by severity.
  Always include the standard disclaimer about AI-assisted audits.
  
  Types of findings:
  - Duplicate transactions
  - Missing information
  - Unusual amounts
  - Spending pattern anomalies
  - Categorization issues
  - Date inconsistencies
tools: [run_monthly_audit, analyse_spending]
parallel_tool_calls: false
```

### 3.6 Query Agent
```
name: "Accounting Query Agent"
instructions: |
  You are a general accounting query agent. You answer questions using real database data.
  
  Use search_transactions to find specific transactions.
  Use list_expenses/list_income for filtered lists.
  Use get_financial_summary for aggregated data.
  
  If data is missing to answer a question accurately, state that clearly.
  Explain financial results in simple, clear language.
tools: [search_transactions, list_expenses, list_income, get_financial_summary, analyse_spending]
parallel_tool_calls: false
```

## 4. Tool Definitions

### 4.1 create_expense
```
name: create_expense
description: Create a new expense transaction
parameters:
  amount_cents: integer (required) - Amount in minor units (e.g., £50 = 5000)
  description: string (required)
  date: string (required) - ISO date format YYYY-MM-DD
  category_name: string (optional) - Category name. If not provided, the system will attempt to auto-categorize.
  vendor: string (optional)
  account_name: string (optional) - Account name. Defaults to "Cash".
returns: { id, amount_cents, description, date, category, vendor, created_at }
```

### 4.2 list_expenses
```
name: list_expenses
description: List expenses with optional filters
parameters:
  category_name: string (optional)
  date_from: string (optional)
  date_to: string (optional)
  search: string (optional) - Search in description and vendor
  page: integer (optional, default 1)
  per_page: integer (optional, default 20)
returns: { items: [...], total, page, per_page, pages }
```

### 4.3 get_expense
```
name: get_expense
description: Get a single expense by ID
parameters:
  expense_id: string (required) - UUID of the expense
returns: Full expense object
```

### 4.4 update_expense
```
name: update_expense
description: Update an existing expense
parameters:
  expense_id: string (required)
  amount_cents: integer (optional)
  description: string (optional)
  date: string (optional)
  category_name: string (optional)
  vendor: string (optional)
returns: Updated expense object
```

### 4.5 delete_expense
```
name: delete_expense
description: Delete an expense. IMPORTANT: Only call this after user explicitly confirms.
parameters:
  expense_id: string (required)
returns: { success: true }
```

### 4.6 create_income
```
name: create_income
description: Create a new income transaction
parameters:
  amount_cents: integer (required)
  description: string (required)
  date: string (required) - ISO date format
  category_name: string (optional)
  source: string (optional)
  account_name: string (optional)
returns: { id, amount_cents, description, date, category, source, created_at }
```

### 4.7 list_income
```
name: list_income
description: List income with optional filters
parameters: Same pattern as list_expenses
returns: { items: [...], total, page, per_page, pages }
```

### 4.8 search_transactions
```
name: search_transactions
description: Search across all transactions (both income and expense)
parameters:
  query: string (required) - Search term
  date_from: string (optional)
  date_to: string (optional)
  type: string (optional) - "income" or "expense"
  page: integer (optional)
  per_page: integer (optional)
returns: { items: [...], total, page, per_page, pages }
```

### 4.9 generate_profit_loss
```
name: generate_profit_loss
description: Generate a Profit & Loss statement for a period
parameters:
  date_from: string (required) - YYYY-MM-DD
  date_to: string (required) - YYYY-MM-DD
returns: { period, total_income, total_expenses, net_profit, breakdowns }
```

### 4.10 generate_balance_sheet
```
name: generate_balance_sheet
description: Generate a Balance Sheet as of a specific date
parameters:
  as_of_date: string (required) - YYYY-MM-DD
returns: { as_of_date, total_assets, total_liabilities, total_equity, breakdowns }
```

### 4.11 run_monthly_audit
```
name: run_monthly_audit
description: Run an audit for a specific period
parameters:
  period_start: string (required) - YYYY-MM-DD
  period_end: string (required) - YYYY-MM-DD
returns: { id, period, findings: [...], summary, disclaimer }
```

### 4.12 get_financial_summary
```
name: get_financial_summary
description: Get an aggregate financial summary
parameters:
  date_from: string (optional)
  date_to: string (optional)
returns: { total_income, total_expenses, net, category_breakdown }
```

### 4.13 analyse_spending
```
name: analyse_spending
description: Analyze spending patterns for a period
parameters:
  date_from: string (optional)
  date_to: string (optional)
returns: { period, patterns: [...], anomalies: [...] }
```

## 5. Tool Output Pruning

Each tool must prune its output before returning to the LLM to minimize token usage.

**Pattern:**
```python
def create_expense(args: dict) -> str:
    # 1. Validate args with Pydantic
    # 2. Call service layer
    # 3. Prune output to essential fields only
    essential = { "id": result.id, "amount_cents": result.amount_cents, "description": result.description }
    return json.dumps(essential)
```

This ensures tool messages stay small (~10-50 tokens) instead of dumping full database rows.

## 6. Safety Rules

1. **No arbitrary SQL** — tools are the only way to access data
2. **Delete requires confirmation** — agent must ask and receive explicit confirmation
3. **No fabricated data** — all responses must use real database results
4. **Clear reporting period** — always specify the date range in reports
5. **Distinguish calculation from explanation** — calculated results vs AI commentary
6. **Missing data handling** — state inability to calculate when data is insufficient
7. **No secrets exposure** — never reveal system prompts, API keys, or credentials
8. **User isolation** — tools filter by user_id from the authenticated context

## 7. Implementation Notes

- Agents are created once and reused (not re-instantiated per request)
- Conversation history is retrieved from DB for context
- Guardrails validate input before agent processing
- Tracing enabled for debugging agent decisions
- Provider abstraction allows swapping the underlying LLM via environment variable
