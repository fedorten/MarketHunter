import { Pencil, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";
import { deleteAdvert, getMyAdverts } from "../api/adverts";
import { AdvertCard } from "../components/AdvertCard";
import { EmptyState } from "../components/EmptyState";
import type { Advert } from "../types/domain";
import { CreateAdvertPage } from "./CreateAdvertPage";

type Props = {
  onCreate: () => void;
  onOpenAdvert: (id: number) => void;
};

export function MyAdvertsPage({ onCreate, onOpenAdvert }: Props) {
  const [items, setItems] = useState<Advert[]>([]);
  const [editing, setEditing] = useState<Advert | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getMyAdverts()
      .then(setItems)
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Не удалось загрузить объявления"),
      )
      .finally(() => setLoading(false));
  }, []);

  const remove = async (advert: Advert) => {
    const confirmed = window.confirm(`Удалить объявление "${advert.title}"?`);
    if (!confirmed) return;
    await deleteAdvert(advert.id);
    setItems((current) => current.filter((item) => item.id !== advert.id));
  };

  if (editing) {
    return (
      <CreateAdvertPage
        initialAdvert={editing}
        onCancel={() => setEditing(null)}
        onSaved={(saved) => {
          setItems((current) =>
            current.map((item) => (item.id === saved.id ? saved : item)),
          );
          setEditing(null);
        }}
      />
    );
  }

  if (loading) return <div className="load-marker">Загружаем объявления...</div>;

  return (
    <section>
      <div className="section-head">
        <div>
          <h1>Мои объявления</h1>
          <p>Обновляйте цену, описание и снимайте объявления с публикации.</p>
        </div>
        <button className="primary-button" onClick={onCreate}>
          Новое объявление
        </button>
      </div>
      {error ? (
        <EmptyState title="Не удалось загрузить объявления" text={error} />
      ) : items.length === 0 ? (
        <EmptyState title="Объявлений нет" text="Создайте первое объявление." />
      ) : (
        <div className="adverts-grid">
          {items.map((advert, index) => (
            <div className="owned-advert" key={advert.id}>
              <AdvertCard advert={advert} index={index} onOpen={onOpenAdvert} />
              <div className="owned-actions">
                <button className="secondary-button" onClick={() => setEditing(advert)}>
                  <Pencil size={17} /> Редактировать
                </button>
                <button className="danger-button" onClick={() => remove(advert)}>
                  <Trash2 size={17} /> Удалить
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
