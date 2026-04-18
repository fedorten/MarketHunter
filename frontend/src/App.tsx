import { useEffect, useState } from 'react'
import { getMe } from './api/auth'
import { clearToken, getToken } from './api/client'
import { BottomNav } from './components/BottomNav'
import { Header } from './components/Header'
import { AdvertPage } from './pages/AdvertPage'
import { AuthPage } from './pages/AuthPage'
import { ChatPage } from './pages/ChatPage'
import { ChatsPage } from './pages/ChatsPage'
import { CreateAdvertPage } from './pages/CreateAdvertPage'
import { FavoritesPage } from './pages/FavoritesPage'
import { FeedPage } from './pages/FeedPage'
import { ProfilePage } from './pages/ProfilePage'
import type { User } from './types/domain'

const protectedPages = new Set(['create', 'favorites', 'chats', 'chat'])

export default function App() {
  const [page, setPage] = useState('feed')
  const [user, setUser] = useState<User | null>(null)
  const [advertId, setAdvertId] = useState<number | null>(null)
  const [chatId, setChatId] = useState<number | null>(null)

  const loadUser = () => {
    if (!getToken()) return
    getMe().then(setUser).catch(() => {
      clearToken()
      setUser(null)
    })
  }

  useEffect(loadUser, [])

  const navigate = (next: string) => {
    if (protectedPages.has(next) && !user && !getToken()) {
      setPage('auth')
      return
    }
    setPage(next)
  }

  const openAdvert = (id: number) => {
    setAdvertId(id)
    setPage('advert')
  }

  const openChat = (id: number) => {
    setChatId(id)
    setPage('chat')
  }

  const content = () => {
    if (page === 'advert' && advertId) return <AdvertPage id={advertId} onBack={() => setPage('feed')} onChat={openChat} />
    if (page === 'create') return <CreateAdvertPage onCreated={openAdvert} />
    if (page === 'favorites') return <FavoritesPage onOpenAdvert={openAdvert} />
    if (page === 'chats') return <ChatsPage onOpenChat={openChat} />
    if (page === 'chat' && chatId) return <ChatPage chatId={chatId} user={user} onBack={() => setPage('chats')} />
    if (page === 'profile') return <ProfilePage user={user} onNavigate={navigate} onLogout={() => setUser(null)} />
    if (page === 'auth') return <AuthPage onLogin={() => { loadUser(); setPage('feed') }} />
    return <FeedPage onOpenAdvert={openAdvert} />
  }

  return (
    <div>
      <Header user={user} current={page} onNavigate={navigate} />
      <main className="app-shell">{content()}</main>
      <BottomNav current={page} onNavigate={navigate} />
    </div>
  )
}
