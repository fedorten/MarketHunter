import { Heart, MapPin } from "lucide-react";
import { mediaUrl } from "../api/client";
import type { Advert } from "../types/domain";
import { fallbackImage } from "../utils/fallbackImages";
import { formatPrice, shortDate } from "../utils/format";

type Props = {
  advert: Advert;
  index: number;
  onOpen: (id: number) => void;
  onLike?: (id: number) => void;
};

export function AdvertCard({ advert, index, onOpen, onLike }: Props) {
  const image = mediaUrl(advert.images_paths?.[0]) || fallbackImage(index);

  return (
    <article className="advert-card">
      <button className="image-button" onClick={() => onOpen(advert.id)}>
        <img src={image} alt={advert.title} loading="lazy" />
      </button>
      <div className="advert-body">
        <div className="row-between">
          <button className="link-title" onClick={() => onOpen(advert.id)}>
            {advert.title}
          </button>
          <button
            className="icon-button"
            onClick={() => onLike?.(advert.id)}
            aria-label="В избранное"
          >
            <Heart size={19} />
          </button>
        </div>
        <strong>{formatPrice(advert.price)}</strong>
        <p>{advert.description || "Без описания"}</p>
        <div className="muted-line">
          <MapPin size={15} />
          <span>
            {advert.location || "Рядом"} · {shortDate(advert.create_date)}
          </span>
        </div>
      </div>
    </article>
  );
}
