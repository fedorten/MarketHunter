import { useEffect, useState } from 'react'
import { getChats } from '../api/chats'
import { mediaUrl } from '../api/client'
import { EmptyState } from '../components/EmptyState'
import type { Chat } from '../types/domain'
import { fallbackImage } from '../utils/fallbackImages'
import { formatPrice } from '../utils/format'

type Props = {
  onOpenChat: (id: number) => void
}

export function ChatsPage({ onOpenChat }: Props) {
  const [chats, setChats] = useState<Chat[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getChats().then(setChats).finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="load-marker">Загружаем чаты...</div>

  return (
    <section>
      <div className="section-head">
        <h1>Сообщения</h1>
        <p>Диалоги по объявлениям собраны в одном месте.</p>
      </div>
      {chats.length === 0 ? (
        <EmptyState title="Сообщений нет" text="Откройте объявление и напишите продавцу." />
      ) : (
        <div className="chat-list">
          {chats.map((chat, index) => (
            <button className="chat-row" key={chat.id} onClick={() => onOpenChat(chat.id)}>
              <img src={mediaUrl(chat.advert_image) || fallbackImage(index)} alt="" />
              <span>
                <strong>{chat.companion.username}</strong>
                <small>{chat.advert_title} · {formatPrice(chat.advert_price)}</small>
                <small>{chat.last_message?.content || 'Диалог создан'}</small>
              </span>
              {chat.unread_count > 0 && <b>{chat.unread_count}</b>}
            </button>
          ))}
        </div>
      )}
    </section>
  )
}
