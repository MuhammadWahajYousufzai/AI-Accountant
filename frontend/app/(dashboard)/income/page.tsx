'use client'

import { useEffect, useState } from 'react'
import { api } from '@/lib/api-client'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Modal } from '@/components/ui/modal'
import type { Income, PaginatedResponse } from '@/types/api'

function fmtCents(c: number) {
  return `£${(c / 100).toLocaleString('en-GB', { minimumFractionDigits: 2 })}`
}

const emptyForm = { amount_cents: 0, description: '', source: '', date: '', category_name: '' }

export default function IncomePage() {
  const [data, setData] = useState<PaginatedResponse<Income> | null>(null)
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [modalOpen, setModalOpen] = useState(false)
  const [form, setForm] = useState(emptyForm)
  const [saving, setSaving] = useState(false)

  const load = async () => {
    setLoading(true)
    try {
      const params: Record<string, string> = { page: String(page) }
      if (search) params.search = search
      const res = await api.income.list(params)
      setData(res)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [page])

  const handleCreate = async () => {
    setSaving(true)
    try {
      await api.income.create({ ...form, amount_cents: Math.round(form.amount_cents * 100) })
      setModalOpen(false)
      setForm(emptyForm)
      load()
    } catch (e: any) {
      alert(e.message)
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this income record?')) return
    try {
      await api.income.delete(id)
      load()
    } catch (e: any) {
      alert(e.message)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Income</h1>
        <Button onClick={() => setModalOpen(true)}>Add Income</Button>
      </div>

      <div className="flex gap-2">
        <Input placeholder="Search income..." value={search} onChange={(e) => setSearch(e.target.value)} className="max-w-xs" />
        <Button variant="secondary" onClick={() => { setPage(1); load() }}>Search</Button>
      </div>

      <Card>
        {loading ? (
          <p className="text-center py-8 text-gray-500">Loading...</p>
        ) : (
          <>
            <div className="space-y-2">
              {data?.items.map((inc) => (
                <div key={inc.id} className="flex items-center justify-between py-3 border-b last:border-0">
                  <div>
                    <p className="text-sm font-medium text-gray-900">{inc.description}</p>
                    <p className="text-xs text-gray-500">{inc.vendor_source} &middot; {inc.date}</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <Badge variant="success">{fmtCents(inc.amount_cents)}</Badge>
                    <button onClick={() => handleDelete(inc.id)} className="text-xs text-red-600 hover:underline">Delete</button>
                  </div>
                </div>
              ))}
              {data?.items.length === 0 && <p className="text-center py-8 text-gray-500">No income found</p>}
            </div>
            {data && data.pages > 1 && (
              <div className="flex justify-center gap-2 mt-4 pt-4 border-t">
                <Button variant="ghost" size="sm" disabled={page <= 1} onClick={() => setPage(page - 1)}>Previous</Button>
                <span className="text-sm text-gray-500 self-center">Page {page} of {data.pages}</span>
                <Button variant="ghost" size="sm" disabled={page >= data.pages} onClick={() => setPage(page + 1)}>Next</Button>
              </div>
            )}
          </>
        )}
      </Card>

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title="Add Income">
        <div className="space-y-4">
          <Input label="Amount (£)" type="number" step="0.01" value={form.amount_cents || ''}
            onChange={(e) => setForm({ ...form, amount_cents: parseFloat(e.target.value) || 0 })} />
          <Input label="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
          <Input label="Source" value={form.source} onChange={(e) => setForm({ ...form, source: e.target.value })} />
          <Input label="Date" type="date" value={form.date} onChange={(e) => setForm({ ...form, date: e.target.value })} />
          <Input label="Category" value={form.category_name} onChange={(e) => setForm({ ...form, category_name: e.target.value })} />
          <div className="flex gap-2 justify-end pt-2">
            <Button variant="secondary" onClick={() => setModalOpen(false)}>Cancel</Button>
            <Button onClick={handleCreate} loading={saving}>Create</Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
