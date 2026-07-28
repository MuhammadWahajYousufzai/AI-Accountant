# Product Requirements Specification

## 1. Product Overview
**AI-Powered Accounting & Finance Assistant** is a full-stack web application that automates day-to-day accounting and bookkeeping tasks. Users interact via a modern dashboard and an AI chat interface to manage expenses, income, financial reports, and audits.

## 2. Target Users
- **Business Owners** — manage finances without accounting expertise
- **Office Administrators** — daily expense and income tracking
- **Accountants** — efficient bookkeeping and reconciliation
- **Chartered Accountants (CAs)** — client management, reports, audits

## 3. User Personas

### Persona A: Small Business Owner (Sarah)
- Manages a retail store with 15 employees
- Needs to track daily expenses and income
- Wants AI to categorize transactions automatically
- No accounting background

### Persona B: Accountant (James)
- Runs a practice with 30 clients
- Needs efficient data entry and report generation
- Uses AI to speed up monthly close
- Needs audit features for client reviews

### Persona C: Office Administrator (Priya)
- Handles day-to-day bookkeeping
- Enters expenses and income manually
- Uses AI chat for quick queries
- Generates monthly reports for management

## 4. Functional Requirements

### FR-01: Authentication
- FR-01.1: User registration with email and password
- FR-01.2: User login with email and password
- FR-01.3: Secure password hashing (bcrypt)
- FR-01.4: JWT token generation and validation
- FR-01.5: Current-user profile endpoint
- FR-01.6: Logout (token invalidation)
- FR-01.7: Protected API routes

### FR-02: Dashboard
- FR-02.1: Display total income, total expenses, net profit/loss
- FR-02.2: Display current cash position
- FR-02.3: Monthly income and expense chart
- FR-02.4: Recent transactions list
- FR-02.5: Expense category breakdown (pie/donut chart)
- FR-02.6: AI-generated financial insights panel

### FR-03: Expense Management
- FR-03.1: Create expense (amount, date, category, description, vendor)
- FR-03.2: View expenses list with pagination
- FR-03.3: Update expense details
- FR-03.4: Delete expense (with confirmation)
- FR-03.5: Filter by category, date range, amount range
- FR-03.6: Search by description or vendor
- FR-03.7: Track daily and monthly expenses

### FR-04: Income Management
- FR-04.1: Create income (amount, date, source, description)
- FR-04.2: View income list with pagination
- FR-04.3: Update income details
- FR-04.4: Delete income (with confirmation)
- FR-04.5: Filter by date range, source, amount
- FR-04.6: Search by description or source

### FR-05: Accounting Records
- FR-05.1: Transaction ledger with all entries
- FR-05.2: Journal entries with double-entry support
- FR-05.3: Account types (asset, liability, equity, income, expense)
- FR-05.4: Category management
- FR-05.5: User data isolation (multi-tenant)

### FR-06: Reports
- FR-06.1: Profit & Loss statement for any date range
- FR-06.2: Balance Sheet as of any date
- FR-06.3: Both use real database data only
- FR-06.4: Expense and income breakdowns in reports
- FR-06.5: Export to PDF (future)

### FR-07: Monthly Audit
- FR-07.1: Detect missing information in transactions
- FR-07.2: Identify duplicate-looking transactions
- FR-07.3: Detect unusual amounts (outliers)
- FR-07.4: Identify unusual spending patterns
- FR-07.5: Flag potential categorization issues
- FR-07.6: Detect date inconsistencies
- FR-07.7: Disclaimer — not a substitute for professional audit

### FR-08: AI Agent
- FR-08.1: Natural language understanding for accounting queries
- FR-08.2: Create accounting entries from natural language
- FR-08.3: Read and query accounting records
- FR-08.4: Update records on request
- FR-08.5: Delete records with explicit confirmation
- FR-08.6: Search transactions by any criteria
- FR-08.7: Answer financial questions using real database data
- FR-08.8: Generate P&L and balance sheet on demand
- FR-08.9: Run monthly audit
- FR-08.10: Analyze spending patterns
- FR-08.11: Detect unusual/anomalous transactions
- FR-08.12: Explain financial results in simple language

### FR-09: AI Chat UI
- FR-09.1: Send messages to AI assistant
- FR-09.2: See assistant responses with formatting
- FR-09.3: See tool/action status indicators
- FR-09.4: View structured financial results (tables, reports)
- FR-09.5: View error messages clearly
- FR-09.6: Continue conversation context across messages
- FR-09.7: Visual distinction between conversation, reports, actions, errors

## 5. Non-Functional Requirements

### NFR-01: Performance
- NFR-01.1: API response time <200ms for CRUD operations (p95)
- NFR-01.2: AI agent response time <10s for simple queries
- NFR-01.3: Report generation <3s for monthly data
- NFR-01.4: Page load time <2s (p95)

### NFR-02: Security
- NFR-02.1: All passwords hashed with bcrypt
- NFR-02.2: JWT tokens with 24h expiry, refresh support
- NFR-02.3: HTTPS-only in production
- NFR-02.4: User data isolation enforced at database level
- NFR-02.5: No secrets in code or commits
- NFR-02.6: CORS configured for frontend origin only
- NFR-02.7: Rate limiting on auth endpoints

### NFR-03: Reliability
- NFR-03.1: All calculations are deterministic
- NFR-03.2: AI agent never fabricates financial data
- NFR-03.3: AI agent never executes arbitrary database queries
- NFR-03.4: Graceful error handling with user-friendly messages
- NFR-03.5: Database transactions for atomic operations

### NFR-04: Usability
- NFR-04.1: Responsive design (desktop + mobile)
- NFR-04.2: Loading states for all async operations
- NFR-04.3: Form validation with clear error messages
- NFR-04.4: Consistent UI patterns throughout

### NFR-05: Maintainability
- NFR-05.1: Typed interfaces throughout (TypeScript, Pydantic)
- NFR-05.2: Separation of concerns (API / service / repository layers)
- NFR-05.3: AI orchestration separate from business logic
- NFR-05.4: Environment-based configuration
- NFR-05.5: Comprehensive test coverage

### NFR-06: Compliance
- NFR-06.1: Audit trail for all AI actions
- NFR-06.2: Clear disclaimer on AI-generated reports
- NFR-06.3: Data export capability (future)

## 6. User Stories

### Authentication
1. As a user, I want to register so I can create an account
2. As a user, I want to log in so I can access my financial data
3. As a user, I want my data to be private and secure

### Expenses
4. As a user, I want to add expenses quickly so I can track spending
5. As a user, I want to search expenses so I can find specific transactions
6. As a user, I want to filter expenses by category and date so I can analyze spending

### Income
7. As a user, I want to record income so I can track earnings
8. As a user, I want to view income by source so I can understand revenue streams

### Reports
9. As a user, I want to generate a P&L so I can see profitability
10. As a user, I want to see a balance sheet so I can understand my financial position
11. As a user, I want a monthly audit so I can catch errors early

### AI Assistant
12. As a user, I want to ask the AI to record transactions so I can save time
13. As a user, I want to ask financial questions so I can get quick answers
14. As a user, I want the AI to generate reports so I don't have to navigate menus
15. As a user, I want the AI to explain variances so I understand my finances

## 7. Acceptance Criteria

### AC-Auth-01: Registration
- Given I am on the registration page
- When I enter a valid email and password (min 8 chars)
- Then my account is created and I receive a JWT token
- And I am redirected to the dashboard

### AC-Auth-02: Login
- Given I have a registered account
- When I enter valid credentials
- Then I receive a JWT token
- And I am redirected to the dashboard

### AC-Expense-01: Create Expense
- Given I am authenticated
- When I submit expense data (amount, category, date, description)
- Then the expense is saved to the database
- And the ledger is updated
- And I see the expense in the list

### AC-AI-01: Natural Language Entry
- Given I am on the AI chat
- When I type "Add office rent of £50,000 for July"
- Then the AI extracts amount (50000), category (rent), date (July)
- And creates the expense in the database
- And confirms with a clear message

### AC-AI-02: Financial Query
- Given I have transactions in the database
- When I ask "How much did we spend on utilities in March?"
- Then the AI queries the database
- And returns the accurate total with breakdown

### AC-Report-01: P&L Statement
- Given I have income and expense data
- When I request a P&L for a specific period
- Then the system calculates total income, total expenses, net profit/loss
- And displays breakdowns by category
- And all figures match database records

### AC-Audit-01: Monthly Audit
- Given I have transaction data
- When I run an audit for a month
- Then the system checks for duplicates, anomalies, missing info, and categorization issues
- And returns a structured report with findings
