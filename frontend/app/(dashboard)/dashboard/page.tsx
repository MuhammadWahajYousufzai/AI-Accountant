'use client'

import { useEffect, useState } from 'react'
import { api } from '@/lib/api-client'
import { Card, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import type { DashboardSummary } from '@/types/api'

function fmtCents(c: number) {
  return `£${(c / 100).toLocaleString('en-GB', { minimumFractionDigits: 2 })}`
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardSummary | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.dashboard.summary()
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="text-center py-12">Loading dashboard...</div>

  if (!data) return <div className="text-center py-12 text-red-600">Failed to load dashboard</div>

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <p className="text-sm text-gray-500 mb-1">Total Income</p>
          <p className="text-2xl font-bold text-green-600">{fmtCents(data.total_income_cents)}</p>
        </Card>
        <Card>
          <p className="text-sm text-gray-500 mb-1">Total Expenses</p>
          <p className="text-2xl font-bold text-red-600">{fmtCents(data.total_expense_cents)}</p>
        </Card>
        <Card>
          <p className="text-sm text-gray-500 mb-1">Net Profit</p>
          <p className={`text-2xl font-bold ${data.net_profit_cents >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {fmtCents(data.net_profit_cents)}
          </p>
        </Card>
        <Card>
          <p className="text-sm text-gray-500 mb-1">Cash Position</p>
          <p className="text-2xl font-bold text-blue-600">{fmtCents(data.cash_position_cents)}</p>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader><CardTitle>Monthly Overview</CardTitle></CardHeader>
          <div className="space-y-3">
            {data.monthly_income.map((m) => (
              <div key={m.month} className="flex items-center justify-between">
                <span className="text-sm text-gray-600">{m.month}</span>
                <div className="flex items-center gap-4">
                  <span className="text-sm text-green-600">+{fmtCents(m.amount_cents)}</span>
                  {data.monthly_expenses.find((e) => e.month === m.month) && (
                    <span className="text-sm text-red-600">
                      -{fmtCents(data.monthly_expenses.find((e) => e.month === m.month)!.amount_cents)}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <CardHeader><CardTitle>Category Breakdown</CardTitle></CardHeader>
          <div className="space-y-2">
            {data.category_breakdown.slice(0, 8).map((c) => (
              <div key={c.category} className="flex items-center justify-between">
                <span className="text-sm text-gray-600">{c.category}</span>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium">{fmtCents(c.amount_cents)}</span>
                  <span className="text-xs text-gray-400">({c.percentage}%)</span>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <Card>
        <CardHeader><CardTitle>Recent Transactions</CardTitle></CardHeader>
        <div className="space-y-2">
          {data.recent_transactions.map((t: any) => (
            <div key={t.id} className="flex items-center justify-between py-2 border-b last:border-0">
              <div className="flex items-center gap-3">
                <Badge variant={t.type === 'income' ? 'success' : 'danger'}>
                  {t.type}
                </Badge>
                <span className="text-sm text-gray-800">{t.description}</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-sm text-gray-500">{t.date}</span>
                <span className={`text-sm font-medium ${t.type === 'income' ? 'text-green-600' : 'text-red-600'}`}>
                  {fmtCents(t.amount_cents)}
                </span>
              </div>
            </div>
          ))}
          {data.recent_transactions.length === 0 && (
            <p className="text-sm text-gray-500 py-4 text-center">No transactions yet</p>
          )}
        </div>
      </Card>

      {data.ai_insights && (
        <Card className="bg-blue-50 border-blue-200">
          <CardHeader><CardTitle className="text-blue-900">AI Insights</CardTitle></CardHeader>
          <p className="text-sm text-blue-800">{data.ai_insights}</p>
        </Card>
      )}
    </div>
  )
}
