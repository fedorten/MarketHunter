import { ArrowLeft, Heart, MessageCircle } from "lucide-react";
import { useEffect, useState } from "react";
import { getAdvert, toggleLike } from "../api/adverts";
import { createChat } from "../api/chats";
import { mediaUrl } from "../api/client";
import type { Advert } from "../types/domain";
import { fallbackImage } from "../utils/fallbackImages";
import { formatPrice, shortDate } from "../utils/format";

type Props = {
  id: number;
  onBack: () => void;
  onChat: (id: number) => void;
};

export function AdvertPage({ id, onBack, onChat }: Props) {
  const [advert, setAdvert] = useState<Advert | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getAdvert(id)
      .then(setAdvert)
      .catch((err) => setError(err.message));
  }, [id]);

  const write = async () => {
    const result = await createChat(id);
    onChat(result.chat_id);
  };

  const like = async () => {
    const result = await toggleLike(id);
    setAdvert((current) =>
      current ? { ...current, likes: result.likes } : current,
    );
  };

  if (error)
    return (
      <div className="empty-state">
        <h2>{error}</h2>
        <button onClick={onBack}>Назад</button>
      </div>
    );
  if (!advert)
    return <div className="load-marker">Загружаем объявление...</div>;

  const image = mediaUrl(advert.images_paths?.[0]) || fallbackImage(advert.id);

  return (
    <article className="details-layout">
      <button className="ghost-button" onClick={onBack}>
        <ArrowLeft size={18} /> Назад
      </button>
      <div className="details-media">
        <img src={image} alt={advert.title} />
      </div>
      <aside className="details-side">
        <p className="muted-text">
          {advert.location || "Рядом"} · {shortDate(advert.create_date)}
        </p>
        <h1>{advert.title}</h1>
        <strong className="price-xl">{formatPrice(advert.price)}</strong>
        <div className="action-row">
          <button className="primary-button" onClick={write}>
            <MessageCircle size={19} /> Написать
          </button>
          <button className="secondary-button" onClick={like}>
            <Heart size={19} /> {advert.likes ?? 0}
          </button>
        </div>
        <p>{advert.description || "Продавец пока не добавил описание."}</p>
        <div className="stats-line">Просмотры: {advert.views ?? 0}</div>
      </aside>
    </article>
  );
}
