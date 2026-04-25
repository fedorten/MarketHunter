import { useEffect, useRef, useState } from "react";
import { getAdverts, toggleLike } from "../api/adverts";
import { AdvertCard } from "../components/AdvertCard";
import { EmptyState } from "../components/EmptyState";
import { SearchFilters } from "../components/SearchFilters";
import type { Advert, AdvertFilters } from "../types/domain";

type Props = {
  onOpenAdvert: (id: number) => void;
};

const initialFilters: AdvertFilters = {
  q: "",
  category: "",
  location: "",
  priceMin: "",
  priceMax: "",
  sortBy: "popular",
};

export function FeedPage({ onOpenAdvert }: Props) {
  const [filters, setFilters] = useState(initialFilters);
  const [applied, setApplied] = useState(initialFilters);
  const [items, setItems] = useState<Advert[]>([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const markerRef = useRef<HTMLDivElement | null>(null);

  const applyFilters = () => {
    setPage(1);
    setItems([]);
    setHasMore(true);
    setApplied({ ...filters });
  };

  useEffect(() => {
    let ignore = false;
    setLoading(true);
    setError("");
    getAdverts(applied, page)
      .then((data) => {
        if (ignore) return;
        setItems((current) => (page === 1 ? data : [...current, ...data]));
        setHasMore(data.length >= 18);
      })
      .catch((err) => {
        if (ignore) return;
        setHasMore(false);
        setError(
          err instanceof Error
            ? err.message
            : "Не удалось загрузить объявления",
        );
      })
      .finally(() => !ignore && setLoading(false));
    return () => {
      ignore = true;
    };
  }, [applied, page]);

  useEffect(() => {
    const marker = markerRef.current;
    if (!marker || !hasMore || loading) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) setPage((value) => value + 1);
      },
      { rootMargin: "500px" },
    );
    observer.observe(marker);
    return () => observer.disconnect();
  }, [hasMore, loading, items.length]);

  const like = async (id: number) => {
    const result = await toggleLike(id);
    setItems((current) =>
      current.map((item) =>
        item.id === id ? { ...item, likes: result.likes } : item,
      ),
    );
  };

  return (
    <>
      <SearchFilters
        filters={filters}
        onChange={setFilters}
        onSubmit={applyFilters}
      />
      <section className="section-head">
        <h1>Вещи рядом</h1>
        <p>
          Лента подстраивается под поиск и спокойно догружает объявления дальше.
        </p>
      </section>
      {error ? (
        <EmptyState title="Не удалось загрузить объявления" text={error} />
      ) : items.length === 0 && !loading ? (
        <EmptyState
          title="Ничего не найдено"
          text="Попробуйте другой запрос или уберите часть фильтров."
        />
      ) : (
        <div className="adverts-grid">
          {items.map((advert, index) => (
            <AdvertCard
              key={`${advert.id}-${index}`}
              advert={advert}
              index={index}
              onOpen={onOpenAdvert}
              onLike={like}
            />
          ))}
        </div>
      )}
      <div ref={markerRef} className="load-marker">
        {loading ? "Загружаем..." : ""}
      </div>
    </>
  );
}
