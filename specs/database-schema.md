# Database Schema Specification

## 1. Design Principles
- Normalized relational model supporting double-entry accounting
- User data isolation via `user_id` foreign key on all data tables
- Audit trail with timestamps on every table
- Appropriate indexes for query performance
- All monetary values stored in minor units (cents/pence) as integers

## 2. Entity Relationship

### 2.1 users
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK, default gen_random_uuid() | |
| email | VARCHAR(255) | UNIQUE, NOT NULL | |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt hash |
| full_name | VARCHAR(255) | NOT NULL | |
| created_at | TIMESTAMPTZ | NOT NULL, default NOW() | |
| updated_at | TIMESTAMPTZ | NOT NULL, default NOW() | |

### 2.2 accounts
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| user_id | UUID | FK → users.id, NOT NULL | |
| name | VARCHAR(255) | NOT NULL | e.g. "Cash", "Accounts Receivable" |
| type | VARCHAR(50) | NOT NULL | asset, liability, equity, income, expense |
| is_system | BOOLEAN | NOT NULL, default FALSE | System accounts are pre-seeded |
| created_at | TIMESTAMPTZ | NOT NULL | |
| updated_at | TIMESTAMPTZ | NOT NULL | |

Index: (user_id, type)

### 2.3 categories
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| user_id | UUID | FK → users.id, NOT NULL | |
| name | VARCHAR(255) | NOT NULL | e.g. "Rent", "Utilities", "Software" |
| type | VARCHAR(10) | NOT NULL | "expense" or "income" |
| is_system | BOOLEAN | NOT NULL, default FALSE | |
| created_at | TIMESTAMPTZ | NOT NULL | |
| updated_at | TIMESTAMPTZ | NOT NULL | |

Index: (user_id, type)
Unique: (user_id, name, type)

### 2.4 transactions
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| user_id | UUID | FK → users.id, NOT NULL | |
| type | VARCHAR(10) | NOT NULL | "income" or "expense" |
| amount_cents | INTEGER | NOT NULL | In minor units |
| currency | VARCHAR(3) | NOT NULL, default 'GBP' | |
| description | TEXT | NOT NULL | |
| vendor_source | VARCHAR(255) | | Vendor (expense) or source (income) |
| date | DATE | NOT NULL | |
| category_id | UUID | FK → categories.id | |
| account_id | UUID | FK → accounts.id | |
| is_reconciled | BOOLEAN | NOT NULL, default FALSE | |
| created_at | TIMESTAMPTZ | NOT NULL | |
| updated_at | TIMESTAMPTZ | NOT NULL | |

Index: (user_id, date), (user_id, category_id), (user_id, type, date)
Index: (user_id, vendor_source) for search

### 2.5 journal_entries
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| user_id | UUID | FK → users.id, NOT NULL | |
| transaction_id | UUID | FK → transactions.id | Link to source transaction |
| entry_date | DATE | NOT NULL | |
| description | TEXT | NOT NULL | |
| created_at | TIMESTAMPTZ | NOT NULL | |

Index: (user_id, entry_date)

### 2.6 ledger_entries
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| user_id | UUID | FK → users.id, NOT NULL | |
| journal_entry_id | UUID | FK → journal_entries.id, NOT NULL | |
| account_id | UUID | FK → accounts.id, NOT NULL | |
| entry_type | VARCHAR(4) | NOT NULL | "debit" or "credit" |
| amount_cents | INTEGER | NOT NULL | |
| created_at | TIMESTAMPTZ | NOT NULL | |

Index: (user_id, account_id), (journal_entry_id)
Constraint: Sum of debits = Sum of credits per journal entry

### 2.7 audit_runs
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| user_id | UUID | FK → users.id, NOT NULL | |
| period_start | DATE | NOT NULL | |
| period_end | DATE | NOT NULL | |
| status | VARCHAR(20) | NOT NULL, default 'completed' | |
| summary | TEXT | | AI-generated summary |
| created_at | TIMESTAMPTZ | NOT NULL | |

Index: (user_id, period_start, period_end)

### 2.8 audit_findings
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| audit_run_id | UUID | FK → audit_runs.id, NOT NULL | |
| finding_type | VARCHAR(50) | NOT NULL | duplicate, missing_info, unusual_amount, pattern_anomaly, categorization_issue, date_inconsistency |
| severity | VARCHAR(10) | NOT NULL | low, medium, high |
| transaction_id | UUID | FK → transactions.id | |
| description | TEXT | NOT NULL | |
| details | JSONB | | Additional context |
| created_at | TIMESTAMPTZ | NOT NULL | |

Index: (audit_run_id), (finding_type), (severity)

### 2.9 ai_conversations
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| user_id | UUID | FK → users.id, NOT NULL | |
| title | VARCHAR(255) | | Auto-generated |
| created_at | TIMESTAMPTZ | NOT NULL | |
| updated_at | TIMESTAMPTZ | NOT NULL | |

Index: (user_id, updated_at)

### 2.10 ai_messages
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| conversation_id | UUID | FK → ai_conversations.id, NOT NULL | |
| role | VARCHAR(20) | NOT NULL | user, assistant, tool |
| content | TEXT | NOT NULL | |
| tool_calls | JSONB | | Tool call metadata |
| tool_results | JSONB | | Tool execution results |
| created_at | TIMESTAMPTZ | NOT NULL | |

Index: (conversation_id, created_at)

## 3. Default System Data

### 3.1 Default Accounts (per user, seeded on registration)
| Name | Type | Description |
|------|------|-------------|
| Cash | asset | Main operating cash account |
| Bank Account | asset | Business bank account |
| Accounts Receivable | asset | Money owed to the business |
| Accounts Payable | liability | Money the business owes |
| Owner's Equity | equity | Owner's capital |
| Retained Earnings | equity | Accumulated profits |
| Revenue | income | Operating revenue |
| Other Income | income | Non-operating income |
| Cost of Goods Sold | expense | Direct costs |
| Operating Expenses | expense | General operating expenses |

### 3.2 Default Expense Categories (per user, seeded on registration)
Rent, Utilities, Salaries, Office Supplies, Software, Marketing, Travel, Meals & Entertainment, Professional Services, Insurance, Maintenance, Transportation, Communication, Other

### 3.3 Default Income Categories (per user, seeded on registration)
Sales, Services, Consulting, Interest, Other

## 4. Key Constraints and Rules
- Every transaction creates a journal entry with at least two ledger entries (debit/credit)
- For expense: debit the expense account, credit the cash/bank account
- For income: debit the cash/bank account, credit the income account
- Amounts stored as integers (cents/pence) to avoid floating-point issues
- All timestamps use TIMESTAMPTZ (UTC)
- user_id ensures data isolation — all queries include user_id filter
