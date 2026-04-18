import { MessageCircle, Plus, Search, UserRound } from 'lucide-react'
import type { User } from '../types/domain'

type Props = {
  user: User | null
  current: string
  onNavigate: (page: string) => void
}

export function Header({ user, current, onNavigate }: Props) {
  return (
    <header className="topbar">
      <button className="brand" onClick={() => onNavigate('feed')} aria-label="На главную">
        <span className="brand-mark">К</span>
        <span>Круг</span>
      </button>

      <nav className="desktop-nav" aria-label="Основная навигация">
        <button className={current === 'feed' ? 'active' : ''} onClick={() => onNavigate('feed')}>
          <Search size={18} /> Поиск
        </button>
        <button className={current === 'create' ? 'active' : ''} onClick={() => onNavigate('create')}>
          <Plus size={18} /> Разместить
        </button>
        <button className={current === 'chats' ? 'active' : ''} onClick={() => onNavigate('chats')}>
          <MessageCircle size={18} /> Чаты
        </button>
        <button className={current === 'profile' ? 'active' : ''} onClick={() => onNavigate('profile')}>
          <UserRound size={18} /> {user ? user.username : 'Войти'}
        </button>
      </nav>
    </header>
  )
}
