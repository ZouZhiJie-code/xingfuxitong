import { Link, Route, Routes } from 'react-router-dom'

import { ConversationPage } from './pages/ConversationPage'
import { DiaryPage } from './pages/DiaryPage'
import { StatsPage } from './pages/StatsPage'

export function App() {
  return (
    <div style={{ margin: '0 auto', maxWidth: 980, padding: 24 }}>
      <h1>幸福设计系统</h1>
      <nav style={{ display: 'flex', gap: 12 }}>
        <Link to="/">复盘对话</Link>
        <Link to="/diary">日记交付</Link>
        <Link to="/stats">数据统计</Link>
      </nav>
      <Routes>
        <Route path="/" element={<ConversationPage />} />
        <Route path="/diary" element={<DiaryPage />} />
        <Route path="/stats" element={<StatsPage />} />
      </Routes>
    </div>
  )
}
