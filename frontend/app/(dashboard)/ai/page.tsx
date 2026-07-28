'use client'

import { useState, useEffect, useRef } from 'react'
import { api } from '@/lib/api-client'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import type { ChatResponse, Conversation } from '@/types/api'

interface Message {
  role: 'user' | 'assistant'
  content: string
  actions?: { type: string; status: string; details?: any }[]
}

export default function AIChatPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [convId, setConvId] = useState<string | undefined>(undefined)
  const endRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    api.ai.conversations().then((res) => setConversations(res.items)).catch(() => {})
  }, [])

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() || loading) return

    const userMsg: Message = { role: 'user', content: input }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const res: ChatResponse = await api.ai.chat({ conversation_id: convId, message: userMsg.content })
      setConvId(res.conversation_id)
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: res.response,
        actions: res.actions,
      }])
    } catch (e: any) {
      setMessages((prev) => [...prev, { role: 'assistant', content: `Error: ${e.message}` }])
    } finally {
      setLoading(false)
    }
  }

  const newConversation = () => {
    setConvId(undefined)
    setMessages([])
  }

  return (
    <div className="flex gap-6 h-[calc(100vh-3rem)]">
      <div className="w-64 flex-shrink-0">
        <Card>
          <CardHeader><CardTitle>Conversations</CardTitle></CardHeader>
          <div className="space-y-2">
            <Button variant="secondary" size="sm" className="w-full" onClick={newConversation}>
              + New Chat
            </Button>
            {conversations.map((c) => (
              <button
                key={c.id}
                onClick={() => setConvId(c.id)}
                className="w-full text-left p-2 rounded text-sm hover:bg-gray-100 truncate"
              >
                {c.title || 'Chat'}
              </button>
            ))}
          </div>
        </Card>
      </div>

      <div className="flex-1 flex flex-col">
        <Card className="flex-1 flex flex-col">
          <CardHeader><CardTitle>AI Accounting Assistant</CardTitle></CardHeader>
          <div className="flex-1 overflow-y-auto space-y-4 p-4">
            {messages.length === 0 && (
              <div className="text-center text-gray-500 py-12">
                <p className="text-lg mb-2">🤖 Ask me anything about your finances</p>
                <p className="text-sm">Try: "Add office rent of £50,000 for July" or "Show me my P&L"</p>
              </div>
            )}
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] p-3 rounded-lg ${
                  msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-900'
                }`}>
                  <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                  {msg.actions && msg.actions.length > 0 && (
                    <div className="mt-2 space-y-1">
                      {msg.actions.map((a, j) => (
                        <div key={j} className="flex items-center gap-2">
                          <Badge variant={a.status === 'success' ? 'success' : 'warning'}>{a.status}</Badge>
                          <span className="text-xs">{a.type.replace(/_/g, ' ')}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 p-3 rounded-lg text-sm text-gray-500">Thinking...</div>
              </div>
            )}
            <div ref={endRef} />
          </div>

          <div className="p-4 border-t flex gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Type your message..."
              disabled={loading}
            />
            <Button onClick={sendMessage} loading={loading}>Send</Button>
          </div>
        </Card>
      </div>
    </div>
  )
}
