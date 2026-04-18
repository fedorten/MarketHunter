import { api, getToken } from './client'
import type { Chat, Message } from '../types/domain'

export function createChat(advertId: number) {
  return api<{ chat_id: number; is_new: boolean }>(`/api/v1/chats/${advertId}`, {
    method: 'POST',
  })
}

export function getChats() {
  return api<Chat[]>('/api/v1/chats/')
}

export function getMessages(chatId: number) {
  return api<Message[]>(`/api/v1/chats/${chatId}/messages`)
}

export function markRead(chatId: number) {
  return api<{ updated: number }>(`/api/v1/chats/${chatId}/read`, {
    method: 'PATCH',
  })
}

export function openChatSocket(chatId: number) {
  const token = getToken()
  const protocol = location.protocol === 'https:' ? 'wss' : 'ws'
  return new WebSocket(`${protocol}://${location.host}/api/v1/chats/ws/${chatId}?token=${token}`)
}
