'use client'

import { useState } from 'react'
import { api } from '@/lib/api-client'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import type { ProfitLossReport, BalanceSheet } from '@/types/api'

function fmtCents(c: number) {
  return `£${(c / 100).toLocaleString('en-GB', { minimumFractionDigits: 2 })}`
}

export default function ReportsPage() {
  const [pl, setPl] = useState<ProfitLossReport | null>(null)
  const [bs, setBs] = useState<BalanceSheet | null>(null)
  const [plFrom, setPlFrom] = useState('')
  const [plTo, setPlTo] = useState('')
  const [bsDate, setBsDate] = useState('')
  const [plLoading, setPlLoading] = useState(false)
  const [bsLoading, setBsLoading] = useState(false)

  const loadPL = async () => {
    if (!plFrom || !plTo) return
    setPlLoading(true)
    try {
      const res = await api.reports.profitLoss({ date_from: plFrom, date_to: plTo })
      setPl(res)
    } catch (e: any) {
      alert(e.message)
    } finally {
      setPlLoading(false)
    }
  }

  const loadBS = async () => {
    if (!bsDate) return
    setBsLoading(true)
    try {
      const res = await api.reports.balanceSheet({ as_of_date: bsDate })
      setBs(res)
    } catch (e: any) {
      alert(e.message)
    } finally {
      setBsLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Reports</h1>

      <Card>
        <CardHeader><CardTitle>Profit & Loss Statement</CardTitle></CardHeader>
        <div className="flex gap-2 mb-4">
          <Input type="date" value={plFrom} onChange={(e) => setPlFrom(e.target.value)} />
          <Input type="date" value={plTo} onChange={(e) => setPlTo(e.target.value)} />
          <Button onClick={loadPL} loading={plLoading}>Generate</Button>
        </div>
        {pl && (
          <div className="space-y-4">
            <div className="text-sm text-gray-500">Period: {pl.period.from} to {pl.period.to}</div>
            <div className="grid grid-cols-3 gap-4">
              <div><p className="text-sm text-gray-500">Income</p><p className="text-lg font-bold text-green-600">{fmtCents(pl.total_income_cents)}</p></div>
              <div><p className="text-sm text-gray-500">Expenses</p><p className="text-lg font-bold text-red-600">{fmtCents(pl.total_expense_cents)}</p></div>
              <div><p className="text-sm text-gray-500">Net Profit</p><p className={`text-lg font-bold ${pl.net_profit_cents >= 0 ? 'text-green-600' : 'text-red-600'}`}>{fmtCents(pl.net_profit_cents)}</p></div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-2">Expense Breakdown</h4>
                {pl.expense_breakdown.map((e) => (
                  <div key={e.category} className="flex justify-between py-1 text-sm"><span>{e.category}</span><span>{fmtCents(e.amount_cents)} ({e.percentage}%)</span></div>
                ))}
              </div>
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-2">Income Breakdown</h4>
                {pl.income_breakdown.map((i) => (
                  <div key={i.category} className="flex justify-between py-1 text-sm"><span>{i.category}</span><span>{fmtCents(i.amount_cents)} ({i.percentage}%)</span></div>
                ))}
              </div>
            </div>
          </div>
        )}
      </Card>

      <Card>
        <CardHeader><CardTitle>Balance Sheet</CardTitle></CardHeader>
        <div className="flex gap-2 mb-4">
          <Input type="date" value={bsDate} onChange={(e) => setBsDate(e.target.value)} />
          <Button onClick={loadBS} loading={bsLoading}>Generate</Button>
        </div>
        {bs && (
          <div className="space-y-4">
            <div className="text-sm text-gray-500">As of: {bs.as_of_date}</div>
            <div className="grid grid-cols-3 gap-4">
              <div><p className="text-sm text-gray-500">Assets</p><p className="text-lg font-bold">{fmtCents(bs.total_assets_cents)}</p></div>
              <div><p className="text-sm text-gray-500">Liabilities</p><p className="text-lg font-bold text-red-600">{fmtCents(bs.total_liabilities_cents)}</p></div>
              <div><p className="text-sm text-gray-500">Equity</p><p className="text-lg font-bold text-green-600">{fmtCents(bs.total_equity_cents)}</p></div>
            </div>
            <div className="grid grid-cols-3 gap-4">
              <div><h4 className="text-sm font-medium text-gray-700 mb-2">Assets</h4>{bs.assets.map((a) => <div key={a.account} className="flex justify-between py-1 text-sm"><span>{a.account}</span><span>{fmtCents(a.amount_cents)}</span></div>)}</div>
              <div><h4 className="text-sm font-medium text-gray-700 mb-2">Liabilities</h4>{bs.liabilities.map((l) => <div key={l.account} className="flex justify-between py-1 text-sm"><span>{l.account}</span><span>{fmtCents(l.amount_cents)}</span></div>)}</div>
              <div><h4 className="text-sm font-medium text-gray-700 mb-2">Equity</h4>{bs.equity.map((e) => <div key={e.account} className="flex justify-between py-1 text-sm"><span>{e.account}</span><span>{fmtCents(e.amount_cents)}</span></div>)}</div>
            </div>
          </div>
        )}
      </Card>
    </div>
  )
}
