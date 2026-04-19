import { LogOut } from "lucide-react";
import { clearToken } from "../api/client";
import type { User } from "../types/domain";

type Props = {
  user: User | null;
  onNavigate: (page: string) => void;
  onLogout: () => void;
};

export function ProfilePage({ user, onNavigate, onLogout }: Props) {
  const logout = () => {
    clearToken();
    onLogout();
  };

  if (!user) {
    return (
      <section className="profile-panel">
        <h1>Профиль</h1>
        <p>
          Войдите, чтобы создавать объявления, писать продавцам и сохранять
          избранное.
        </p>
        <button className="primary-button" onClick={() => onNavigate("auth")}>
          Войти
        </button>
      </section>
    );
  }

  return (
    <section className="profile-panel">
      <h1>{user.username}</h1>
      <p>{user.phone}</p>
      <p>{user.email || "Email не указан"}</p>
      <div className="profile-actions">
        <button onClick={() => onNavigate("create")}>
          Разместить объявление
        </button>
        <button onClick={() => onNavigate("favorites")}>Избранное</button>
        <button onClick={() => onNavigate("chats")}>Сообщения</button>
      </div>
      <button className="secondary-button" onClick={logout}>
        <LogOut size={18} /> Выйти
      </button>
    </section>
  );
}
