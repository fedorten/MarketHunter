import { ArrowLeft, Send } from "lucide-react";
import { FormEvent, useEffect, useRef, useState } from "react";
import { getMessages, markRead, openChatSocket, sendMessage } from "../api/chats";
import type { Message, User } from "../types/domain";

type Props = {
  chatId: number;
  user: User | null;
  onBack: () => void;
};

export function ChatPage({ chatId, user, onBack }: Props) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [text, setText] = useState("");
  const [status, setStatus] = useState("Подключаемся...");
  const [error, setError] = useState("");
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    setError("");
    setStatus("Подключаемся...");
    getMessages(chatId).then(setMessages).catch((err) => {
      setError(err instanceof Error ? err.message : "Не удалось загрузить сообщения");
    });
    markRead(chatId).catch(() => undefined);
    const socket = openChatSocket(chatId);
    socketRef.current = socket;
    socket.onopen = () => setStatus("");
    socket.onmessage = (event) => {
      setMessages((current) => [...current, JSON.parse(event.data)]);
    };
    socket.onerror = () => setError("Соединение с чатом не установлено");
    socket.onclose = () => setStatus("Соединение закрыто");
    return () => {
      socketRef.current = null;
      socket.close();
    };
  }, [chatId]);

  const send = async (event: FormEvent) => {
    event.preventDefault();
    const content = text.trim();
    if (!content) return;
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      setError("");
      socketRef.current.send(content);
      setText("");
      return;
    }
    try {
      const saved = await sendMessage(chatId, content);
      setMessages((current) => [...current, saved]);
      setError("");
      setText("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Не удалось отправить сообщение");
    }
  };

  return (
    <section className="chat-page">
      <button className="ghost-button" onClick={onBack}>
        <ArrowLeft size={18} /> Все чаты
      </button>
      <div className="messages-pane">
        {messages.map((message) => (
          <div
            key={message.id}
            className={
              message.sender_id === user?.id ? "message mine" : "message"
            }
          >
            {message.content}
          </div>
        ))}
        {status && <div className="muted-text">{status}</div>}
        {error && <div className="error-text">{error}</div>}
      </div>
      <form className="message-form" onSubmit={send}>
        <input
          value={text}
          onChange={(event) => setText(event.target.value)}
          placeholder="Сообщение"
        />
        <button className="primary-button">
          <Send size={18} />
        </button>
      </form>
    </section>
  );
}
