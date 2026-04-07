import { FormEvent, useEffect, useMemo, useState } from 'react'

import { apiClient } from '../services/api'

type Role = 'assistant' | 'user'

type ChatBubble = {
  id: string
  role: Role
  content: string
}

type SessionState = {
  current_element: string
  completed_elements: string[]
  pending_elements: string[]
}

const defaultUserId = 'demo-user'
const defaultSessionId = 'session-001'

export function ConversationPage() {
  const [input, setInput] = useState('')
  const [isSending, setIsSending] = useState(false)
  const [messages, setMessages] = useState<ChatBubble[]>([
    {
      id: 'assistant-welcome',
      role: 'assistant',
      content: '你好，我们先从“意义”维度开始。请说一个今天你做过的客观行为事实。',
    },
  ])
  const [sessionState, setSessionState] = useState<SessionState | null>(null)

  const completedCount = useMemo(() => sessionState?.completed_elements.length ?? 0, [sessionState])

  async function loadSessionState() {
    const { data } = await apiClient.get<SessionState>(`/chat/session/${defaultUserId}/${defaultSessionId}`)
    setSessionState(data)
  }

  useEffect(() => {
    void loadSessionState()
  }, [])

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const text = input.trim()
    if (!text || isSending) return

    setIsSending(true)
    setInput('')
    const userId = `user-${Date.now()}`
    const assistantId = `assistant-${Date.now()}`

    setMessages((prev) => [...prev, { id: userId, role: 'user', content: text }, { id: assistantId, role: 'assistant', content: '' }])

    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'}/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: defaultUserId, session_id: defaultSessionId, message: text }),
      })

      if (!response.body) {
        throw new Error('empty stream body')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder('utf-8')
      let done = false
      let buffer = ''

      while (!done) {
        const { value, done: streamDone } = await reader.read()
        done = streamDone
        if (!value) continue

        buffer += decoder.decode(value, { stream: true })
        const segments = buffer.split('\n\n')
        buffer = segments.pop() ?? ''

        segments.forEach((segment) => {
          if (!segment.startsWith('data: ')) return
          const payload = segment.replace('data: ', '')
          if (payload === '[DONE]') return
          setMessages((prev) =>
            prev.map((msg) => (msg.id === assistantId ? { ...msg, content: `${msg.content}${payload}` } : msg)),
          )
        })
      }

      await loadSessionState()
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: `assistant-error-${Date.now()}`,
          role: 'assistant',
          content: '网络异常，请稍后重试。',
        },
      ])
    } finally {
      setIsSending(false)
    }
  }

  return (
    <section style={{ marginTop: 20 }}>
      <h2>沉浸式复盘页</h2>
      <p>已完成维度：{completedCount} / 8</p>
      <p>当前维度：{sessionState?.current_element ?? '加载中...'}</p>

      <div style={{ border: '1px solid #ddd', borderRadius: 12, minHeight: 320, padding: 12, marginBottom: 12 }}>
        {messages.map((message) => (
          <div key={message.id} style={{ marginBottom: 10, textAlign: message.role === 'user' ? 'right' : 'left' }}>
            <span
              style={{
                display: 'inline-block',
                background: message.role === 'user' ? '#d5f3ff' : '#f4f4f4',
                borderRadius: 10,
                padding: '8px 12px',
                maxWidth: '80%',
              }}
            >
              {message.content || '...'}
            </span>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 8 }}>
        <input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="请输入今天的客观行为事实"
          style={{ flex: 1, padding: '10px 12px', borderRadius: 8, border: '1px solid #ccc' }}
        />
        <button type="submit" disabled={isSending}>
          {isSending ? '发送中...' : '发送'}
        </button>
      </form>
    </section>
  )
}
