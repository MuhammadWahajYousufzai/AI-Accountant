# API Contracts

## 1. Authentication

### POST /api/v1/auth/register
**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "full_name": "John Doe"
}
```
**Response (201):**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe"
  }
}
```
**Errors:** 409 (email exists), 422 (validation)

### POST /api/v1/auth/login
**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```
**Response (200):**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "user": { "id": "uuid", "email": "...", "full_name": "..." }
}
```
**Errors:** 401 (invalid credentials)

### GET /api/v1/auth/me
**Headers:** Authorization: Bearer <token>
**Response (200):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "created_at": "2026-07-28T12:00:00Z"
}
```
**Errors:** 401 (unauthorized)

## 2. Expenses

### GET /api/v1/expenses
**Query Params:** page, per_page, category_id, date_from, date_to, amount_min, amount_max, search
**Response (200):**
```json
{
  "items": [
    {
      "id": "uuid",
      "amount_cents": 5000000,
      "currency": "GBP",
      "description": "Office rent for July",
      "vendor": "Landlord Ltd",
      "date": "2026-07-01",
      "category": { "id": "uuid", "name": "Rent" },
      "account": { "id": "uuid", "name": "Cash" },
      "is_reconciled": false,
      "created_at": "2026-07-01T10:00:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "per_page": 20,
  "pages": 3
}
```

### POST /api/v1/expenses
**Request:**
```json
{
  "amount_cents": 5000000,
  "currency": "GBP",
  "description": "Office rent for July",
  "vendor": "Landlord Ltd",
  "date": "2026-07-01",
  "category_id": "uuid",
  "account_id": "uuid"
}
```
**Response (201):** Full expense object

### GET /api/v1/expenses/{id}
**Response (200):** Full expense object

### PUT /api/v1/expenses/{id}
**Request:** Same as POST (partial update allowed)
**Response (200):** Updated expense object

### DELETE /api/v1/expenses/{id}
**Response (204):** No content

## 3. Income

### GET /api/v1/income
**Query Params:** page, per_page, category_id, date_from, date_to, amount_min, amount_max, search
**Response (200):**
```json
{
  "items": [
    {
      "id": "uuid",
      "amount_cents": 25000000,
      "currency": "GBP",
      "description": "Invoice #123 - Consulting services",
      "source": "Client ABC",
      "date": "2026-07-15",
      "category": { "id": "uuid", "name": "Services" },
      "account": { "id": "uuid", "name": "Bank Account" },
      "is_reconciled": false,
      "created_at": "2026-07-15T14:00:00Z"
    }
  ],
  "total": 30,
  "page": 1,
  "per_page": 20,
  "pages": 2
}
```

### POST /api/v1/income
**Request:**
```json
{
  "amount_cents": 25000000,
  "currency": "GBP",
  "description": "Invoice #123 - Consulting services",
  "source": "Client ABC",
  "date": "2026-07-15",
  "category_id": "uuid",
  "account_id": "uuid"
}
```
**Response (201):** Full income object

### GET /api/v1/income/{id}
**Response (200):** Full income object

### PUT /api/v1/income/{id}
**Response (200):** Updated income object

### DELETE /api/v1/income/{id}
**Response (204):** No content

## 4. Transactions (Ledger)

### GET /api/v1/transactions
**Query Params:** page, per_page, type (income/expense), date_from, date_to, category_id, search
**Response (200):**
```json
{
  "items": [
    {
      "id": "uuid",
      "type": "expense",
      "amount_cents": 5000000,
      "currency": "GBP",
      "description": "Office rent for July",
      "vendor_source": "Landlord Ltd",
      "date": "2026-07-01",
      "category": { "id": "uuid", "name": "Rent", "type": "expense" },
      "created_at": "2026-07-01T10:00:00Z"
    }
  ],
  "total": 80,
  "page": 1,
  "per_page": 20,
  "pages": 4
}
```

## 5. Accounts

### GET /api/v1/accounts
**Response (200):**
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "Cash",
      "type": "asset",
      "balance_cents": 10000000,
      "is_system": true
    }
  ]
}
```

### POST /api/v1/accounts
**Request:** `{ "name": "...", "type": "asset" }`
**Response (201):** Full account object

## 6. Categories

### GET /api/v1/categories
**Response (200):**
```json
{
  "items": [
    { "id": "uuid", "name": "Rent", "type": "expense", "is_system": true }
  ]
}
```

### POST /api/v1/categories
**Request:** `{ "name": "...", "type": "expense" }`
**Response (201):** Full category object

## 7. Reports

### POST /api/v1/reports/profit-loss
**Request:**
```json
{
  "date_from": "2026-07-01",
  "date_to": "2026-07-31"
}
```
**Response (200):**
```json
{
  "period": { "from": "2026-07-01", "to": "2026-07-31" },
  "total_income_cents": 25000000,
  "total_expense_cents": 15000000,
  "net_profit_cents": 10000000,
  "currency": "GBP",
  "expense_breakdown": [
    { "category": "Rent", "amount_cents": 5000000, "percentage": 33.3 },
    { "category": "Salaries", "amount_cents": 8000000, "percentage": 53.3 }
  ],
  "income_breakdown": [
    { "category": "Services", "amount_cents": 25000000, "percentage": 100 }
  ]
}
```

### POST /api/v1/reports/balance-sheet
**Request:**
```json
{
  "as_of_date": "2026-07-31"
}
```
**Response (200):**
```json
{
  "as_of_date": "2026-07-31",
  "total_assets_cents": 50000000,
  "total_liabilities_cents": 15000000,
  "total_equity_cents": 35000000,
  "assets": [
    { "account": "Cash", "amount_cents": 30000000 },
    { "account": "Bank Account", "amount_cents": 20000000 }
  ],
  "liabilities": [
    { "account": "Accounts Payable", "amount_cents": 15000000 }
  ],
  "equity": [
    { "account": "Owner's Equity", "amount_cents": 35000000 }
  ]
}
```

## 8. Audit

### POST /api/v1/audit/run
**Request:**
```json
{
  "period_start": "2026-07-01",
  "period_end": "2026-07-31"
}
```
**Response (200):**
```json
{
  "id": "uuid",
  "period": { "start": "2026-07-01", "end": "2026-07-31" },
  "status": "completed",
  "findings": [
    {
      "type": "duplicate",
      "severity": "high",
      "transaction_id": "uuid",
      "description": "Possible duplicate: Two expenses of £500 to 'Office Supplies Co' on 2026-07-15"
    },
    {
      "type": "unusual_amount",
      "severity": "medium",
      "transaction_id": "uuid",
      "description": "Expense of £15,000 to 'New Vendor' is 3x above average"
    }
  ],
  "summary": "Audit found 2 issues: 1 potential duplicate and 1 unusual transaction.",
  "disclaimer": "This is an AI-assisted audit and does not replace professional audit or legal/tax advice."
}
```

## 9. AI Chat

### POST /api/v1/ai/chat
**Request:**
```json
{
  "conversation_id": "uuid (optional, creates new if omitted)",
  "message": "Add office rent of £50,000 for July"
}
```
**Response (200):**
```json
{
  "conversation_id": "uuid",
  "response": "I've added office rent of £50,000 for July 2026 to your expenses. The transaction has been posted to the Rent category and your Cash account has been debited.",
  "actions": [
    {
      "type": "create_expense",
      "status": "success",
      "details": {
        "amount_cents": 5000000,
        "category": "Rent",
        "date": "2026-07-01",
        "description": "Office rent for July"
      }
    }
  ],
  "tool_calls": [
    { "tool": "create_expense", "args": { "...": "..." }, "result": "..." }
  ]
}
```

### GET /api/v1/ai/conversations
**Response (200):**
```json
{
  "items": [
    {
      "id": "uuid",
      "title": "Expense queries",
      "message_count": 5,
      "updated_at": "2026-07-28T12:00:00Z"
    }
  ]
}
```

### GET /api/v1/ai/conversations/{id}/messages
**Response (200):**
```json
{
  "items": [
    {
      "id": "uuid",
      "role": "user",
      "content": "Add office rent of £50,000 for July",
      "created_at": "2026-07-28T12:00:00Z"
    },
    {
      "id": "uuid",
      "role": "assistant",
      "content": "I've added office rent...",
      "tool_calls": [...],
      "created_at": "2026-07-28T12:00:01Z"
    }
  ]
}
```

## 10. Dashboard

### GET /api/v1/dashboard/summary
**Query Params:** month (YYYY-MM, defaults to current)
**Response (200):**
```json
{
  "total_income_cents": 25000000,
  "total_expense_cents": 15000000,
  "net_profit_cents": 10000000,
  "cash_position_cents": 50000000,
  "monthly_income": [
    { "month": "2026-07", "amount_cents": 25000000 }
  ],
  "monthly_expenses": [
    { "month": "2026-07", "amount_cents": 15000000 }
  ],
  "recent_transactions": [...],
  "category_breakdown": [
    { "category": "Rent", "amount_cents": 5000000, "percentage": 33.3 }
  ],
  "ai_insights": "Your expenses this month are in line with the previous month..."
}
```

## 11. Common Error Responses

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "amount_cents"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 401 Unauthorized
```json
{ "detail": "Not authenticated" }
```

### 403 Forbidden
```json
{ "detail": "Not enough permissions" }
```

### 404 Not Found
```json
{ "detail": "Expense not found" }
```

### 409 Conflict
```json
{ "detail": "An account with this name already exists" }
```
