export interface User {
  id: string
  email: string
  full_name: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export interface Category {
  id: string
  name: string
  type: 'expense' | 'income'
  is_system: boolean
}

export interface Account {
  id: string
  name: string
  type: string
  balance_cents: number
  is_system: boolean
}

export interface Transaction {
  id: string
  type: 'income' | 'expense'
  amount_cents: number
  currency: string
  description: string
  vendor_source?: string
  date: string
  category?: { id: string; name: string }
  created_at: string
}

export interface Expense extends Transaction {}
export interface Income extends Transaction {}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  per_page: number
  pages: number
}

export interface ProfitLossReport {
  period: { from: string; to: string }
  total_income_cents: number
  total_expense_cents: number
  net_profit_cents: number
  currency: string
  expense_breakdown: { category: string; amount_cents: number; percentage: number }[]
  income_breakdown: { category: string; amount_cents: number; percentage: number }[]
}

export interface BalanceSheet {
  as_of_date: string
  total_assets_cents: number
  total_liabilities_cents: number
  total_equity_cents: number
  assets: { account: string; amount_cents: number }[]
  liabilities: { account: string; amount_cents: number }[]
  equity: { account: string; amount_cents: number }[]
}

export interface AuditFinding {
  type: string
  severity: string
  transaction_id?: string
  description: string
}

export interface AuditRun {
  id: string
  period: { start: string; end: string }
  status: string
  findings: AuditFinding[]
  summary: string
  disclaimer: string
}

export interface DashboardSummary {
  total_income_cents: number
  total_expense_cents: number
  net_profit_cents: number
  cash_position_cents: number
  monthly_income: { month: string; amount_cents: number }[]
  monthly_expenses: { month: string; amount_cents: number }[]
  recent_transactions: Transaction[]
  category_breakdown: { category: string; amount_cents: number; percentage: number }[]
  ai_insights: string
}

export interface ChatResponse {
  conversation_id: string
  response: string
  actions: { type: string; status: string; details?: any }[]
}

export interface Conversation {
  id: string
  title?: string
  message_count: number
  updated_at: string
}

export interface Message {
  id: string
  role: string
  content: string
  tool_calls?: any
  created_at: string
}
