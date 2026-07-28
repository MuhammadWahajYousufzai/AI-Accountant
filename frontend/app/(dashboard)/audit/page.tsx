'use client'

import { useState } from 'react'
import { api } from '@/lib/api-client'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import type { AuditRun } from '@/types/api'

export default function AuditPage() {
  const [audit, setAudit] = useState<AuditRun | null>(null)
  const [periodStart, setPeriodStart] = useState('')
  const [periodEnd, setPeriodEnd] = useState('')
  const [loading, setLoading] = useState(false)

  const runAudit = async () => {
    if (!periodStart || !periodEnd) return
    setLoading(true)
    try {
      const res = await api.audit.run({ period_start: periodStart, period_end: periodEnd })
      setAudit(res)
    } catch (e: any) {
      alert(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Monthly Audit</h1>

      <Card>
        <CardHeader><CardTitle>Run Audit</CardTitle></CardHeader>
        <div className="flex gap-2 mb-4">
          <Input type="date" value={periodStart} onChange={(e) => setPeriodStart(e.target.value)} />
          <Input type="date" value={periodEnd} onChange={(e) => setPeriodEnd(e.target.value)} />
          <Button onClick={runAudit} loading={loading}>Run Audit</Button>
        </div>
      </Card>

      {audit && (
        <Card>
          <CardHeader>
            <CardTitle>Audit Results</CardTitle>
            <p className="text-sm text-gray-500">
              Period: {audit.period.start} to {audit.period.end}
            </p>
          </CardHeader>

          <div className="mb-4 p-3 bg-gray-50 rounded-lg">
            <p className="text-sm font-medium">{audit.summary}</p>
          </div>

          {audit.findings.length === 0 ? (
            <p className="text-sm text-gray-500 py-4 text-center">No issues found.</p>
          ) : (
            <div className="space-y-3">
              {audit.findings.map((f, i) => (
                <div key={i} className="flex items-start gap-3 p-3 border rounded-lg">
                  <Badge variant={f.severity === 'high' ? 'danger' : f.severity === 'medium' ? 'warning' : 'default'}>
                    {f.severity}
                  </Badge>
                  <div>
                    <p className="text-sm font-medium">{f.type.replace(/_/g, ' ')}</p>
                    <p className="text-sm text-gray-600">{f.description}</p>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="mt-4 p-3 bg-yellow-50 rounded-lg">
            <p className="text-xs text-yellow-800">{audit.disclaimer}</p>
          </div>
        </Card>
      )}
    </div>
  )
}
