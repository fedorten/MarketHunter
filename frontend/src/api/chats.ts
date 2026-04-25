import { api, getToken, websocketUrl } from "./client";
import type { Chat, Message } from "../types/domain";

export function createChat(advertId: number) {
  return api<{ chat_id: number; is_new: boolean }>(
    `/api/v1/chats/${advertId}`,
    {
      method: "POST",
    },
  );
}

export function getChats() {
  return api<Chat[]>("/api/v1/chats/");
}

export function getMessages(chatId: number) {
  return api<Message[]>(`/api/v1/chats/${chatId}/messages`);
}

export function sendMessage(chatId: number, content: string) {
  return api<Message>(`/api/v1/chats/${chatId}/messages`, {
    method: "POST",
    body: JSON.stringify({ content }),
  });
}

export function markRead(chatId: number) {
  return api<{ updated: number }>(`/api/v1/chats/${chatId}/read`, {
    method: "PATCH",
  });
}

export function openChatSocket(chatId: number) {
  const token = getToken();
  const params = new URLSearchParams();
  if (token) params.set("token", token);
  return new WebSocket(
    websocketUrl(`/api/v1/chats/ws/${chatId}?${params.toString()}`),
  );
}
