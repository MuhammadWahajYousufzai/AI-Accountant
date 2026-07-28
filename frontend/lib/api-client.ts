import type {
  AuthResponse, PaginatedResponse, Expense, Income, Transaction,
  ProfitLossReport, BalanceSheet, AuditRun, DashboardSummary,
  ChatResponse, Conversation, Message, Category, Account,
} from '@/types/api'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

function getToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('token')
  }
  return null
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken()
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...((options.headers as Record<string, string>) || {}),
  }
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const res = await fetch(`${API_URL}/api/v1${path}`, {
    ...options,
    headers,
  })

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Unknown error' }))
    if (res.status === 401 && typeof window !== 'undefined') {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    throw new Error(error.detail || `HTTP ${res.status}`)
  }

  if (res.status === 204) return undefined as T
  return res.json()
}

export const api = {
  auth: {
    register: (data: { email: string; password: string; full_name: string }) =>
      request<AuthResponse>('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
    login: (data: { email: string; password: string }) =>
      request<AuthResponse>('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
    me: () => request<any>('/auth/me'),
  },

  expenses: {
    list: (params?: Record<string, string>) => {
      const qs = params ? '?' + new URLSearchParams(params).toString() : ''
      return request<PaginatedResponse<Expense>>(`/expenses${qs}`)
    },
    create: (data: any) =>
      request<Expense>('/expenses', { method: 'POST', body: JSON.stringify(data) }),
    get: (id: string) => request<Expense>(`/expenses/${id}`),
    update: (id: string, data: any) =>
      request<Expense>(`/expenses/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (id: string) =>
      request<void>(`/expenses/${id}`, { method: 'DELETE' }),
  },

  income: {
    list: (params?: Record<string, string>) => {
      const qs = params ? '?' + new URLSearchParams(params).toString() : ''
      return request<PaginatedResponse<Income>>(`/income${qs}`)
    },
    create: (data: any) =>
      request<Income>('/income', { method: 'POST', body: JSON.stringify(data) }),
    get: (id: string) => request<Income>(`/income/${id}`),
    update: (id: string, data: any) =>
      request<Income>(`/income/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (id: string) =>
      request<void>(`/income/${id}`, { method: 'DELETE' }),
  },

  transactions: {
    list: (params?: Record<string, string>) => {
      const qs = params ? '?' + new URLSearchParams(params).toString() : ''
      return request<PaginatedResponse<Transaction>>(`/transactions${qs}`)
    },
  },

  reports: {
    profitLoss: (data: { date_from: string; date_to: string }) =>
      request<ProfitLossReport>('/reports/profit-loss', { method: 'POST', body: JSON.stringify(data) }),
    balanceSheet: (data: { as_of_date: string }) =>
      request<BalanceSheet>('/reports/balance-sheet', { method: 'POST', body: JSON.stringify(data) }),
    dashboard: (month?: string) =>
      request<DashboardSummary>(`/reports/dashboard${month ? `?month=${month}` : ''}`),
  },

  dashboard: {
    summary: (month?: string) =>
      request<DashboardSummary>(`/dashboard/summary${month ? `?month=${month}` : ''}`),
  },

  audit: {
    run: (data: { period_start: string; period_end: string }) =>
      request<AuditRun>('/audit/run', { method: 'POST', body: JSON.stringify(data) }),
  },

  ai: {
    chat: (data: { conversation_id?: string; message: string }) =>
      request<ChatResponse>('/ai/chat', { method: 'POST', body: JSON.stringify(data) }),
    conversations: () => request<{ items: Conversation[] }>('/ai/conversations'),
    messages: (id: string) => request<{ items: Message[] }>(`/ai/conversations/${id}/messages`),
  },

  categories: {
    list: () => request<{ items: Category[] }>('/categories'),
    create: (data: { name: string; type: string }) =>
      request<Category>('/categories', { method: 'POST', body: JSON.stringify(data) }),
  },

  accounts: {
    list: () => request<{ items: Account[] }>('/accounts'),
    create: (data: { name: string; type: string }) =>
      request<Account>('/accounts', { method: 'POST', body: JSON.stringify(data) }),
  },
}
