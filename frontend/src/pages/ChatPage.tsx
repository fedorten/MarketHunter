import { ArrowLeft, Send } from 'lucide-react'
import { FormEvent, useEffect, useRef, useState } from 'react'
import { getMessages, markRead, openChatSocket } from '../api/chats'
import type { Message, User } from '../types/domain'

type Props = {
  chatId: number
  user: User | null
  onBack: () => void
}

export function ChatPage({ chatId, user, onBack }: Props) {
  const [messages, setMessages] = useState<Message[]>([])
  const [text, setText] = useState('')
  const socketRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    getMessages(chatId).then(setMessages)
    markRead(chatId).catch(() => undefined)
    const socket = openChatSocket(chatId)
    socketRef.current = socket
    socket.onmessage = (event) => {
      setMessages((current) => [...current, JSON.parse(event.data)])
    }
    return () => socket.close()
  }, [chatId])

  const send = (event: FormEvent) => {
    event.preventDefault()
    if (!text.trim()) return
    socketRef.current?.send(text.trim())
    setText('')
  }

  return (
    <section className="chat-page">
      <button className="ghost-button" onClick={onBack}><ArrowLeft size={18} /> Все чаты</button>
      <div className="messages-pane">
        {messages.map((message) => (
          <div key={message.id} className={message.sender_id === user?.id ? 'message mine' : 'message'}>
            {message.content}
          </div>
        ))}
      </div>
      <form className="message-form" onSubmit={send}>
        <input value={text} onChange={(event) => setText(event.target.value)} placeholder="Сообщение" />
        <button className="primary-button"><Send size={18} /></button>
      </form>
    </section>
  )
}
