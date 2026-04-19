import { Heart, Home, MessageCircle, Plus, UserRound } from "lucide-react";

type Props = {
  current: string;
  onNavigate: (page: string) => void;
};

const items = [
  ["feed", Home, "Главная"],
  ["favorites", Heart, "Избранное"],
  ["create", Plus, "Создать"],
  ["chats", MessageCircle, "Чаты"],
  ["profile", UserRound, "Профиль"],
] as const;

export function BottomNav({ current, onNavigate }: Props) {
  return (
    <nav className="bottom-nav" aria-label="Мобильная навигация">
      {items.map(([page, Icon, label]) => (
        <button
          key={page}
          className={current === page ? "active" : ""}
          onClick={() => onNavigate(page)}
        >
          <Icon size={20} />
          <span>{label}</span>
        </button>
      ))}
    </nav>
  );
}
