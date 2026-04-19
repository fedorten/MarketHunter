import { api, setToken } from "./client";
import type { User } from "../types/domain";

export async function login(phone: string, password: string) {
  const body = new URLSearchParams();
  body.set("username", phone.trim());
  body.set("password", password);

  const result = await api<{ access_token: string }>("/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  setToken(result.access_token);
  return result;
}

export function register(payload: {
  username: string;
  phone: string;
  password: string;
  email?: string;
}) {
  return api<{ msg: string }>("/registration", {
    method: "POST",
    body: JSON.stringify({
      ...payload,
      username: payload.username.trim(),
      phone: payload.phone.trim(),
      email: payload.email?.trim() || undefined,
    }),
  });
}

export function getMe() {
  return api<User>("/api/v1/users/me");
}
