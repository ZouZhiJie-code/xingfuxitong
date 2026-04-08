import { FormEvent, useEffect, useState } from 'react'

import { apiClient } from '../services/api'

export function KeySettingsPage() {
  const [userId, setUserId] = useState('demo-user')
  const [apiKey, setApiKey] = useState('')
  const [status, setStatus] = useState('')
  const [masked, setMasked] = useState<string | null>(null)

  async function loadStatus(currentUserId: string) {
    const { data } = await apiClient.get(`/keys/minimax/${currentUserId}`)
    setMasked(data?.key_masked ?? null)
  }

  useEffect(() => {
    void loadStatus(userId)
  }, [userId])

  async function handleSave(event: FormEvent) {
    event.preventDefault()
    await apiClient.post('/keys/minimax', { user_id: userId, api_key: apiKey })
    setStatus('已保存')
    setApiKey('')
    await loadStatus(userId)
  }

  async function handleVerify() {
    const { data } = await apiClient.post('/keys/minimax/verify', { user_id: userId })
    setStatus(String(data?.message ?? ''))
  }

  return (
    <section style={{ marginTop: 20 }}>
      <h2>BYOK 设置页</h2>
      <p>请为当前用户配置 MiniMax API Key（仅服务端保存加密值）。</p>
      <form onSubmit={handleSave} style={{ display: 'grid', gap: 10, maxWidth: 680 }}>
        <input value={userId} onChange={(e) => setUserId(e.target.value)} placeholder="user_id" />
        <input value={apiKey} onChange={(e) => setApiKey(e.target.value)} placeholder="输入 MiniMax API Key" />
        <div style={{ display: 'flex', gap: 8 }}>
          <button type="submit">保存 Key</button>
          <button type="button" onClick={handleVerify}>
            验证 Key
          </button>
        </div>
      </form>
      <p>当前掩码：{masked ?? '未配置'}</p>
      <p>状态：{status || '-'}</p>
    </section>
  )
}
