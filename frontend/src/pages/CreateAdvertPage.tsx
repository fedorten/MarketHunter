import { ImagePlus } from "lucide-react";
import { FormEvent, useState } from "react";
import { createAdvert, updateAdvert, uploadImage } from "../api/adverts";
import type { Advert } from "../types/domain";

type Props = {
  initialAdvert?: Advert;
  onCancel?: () => void;
  onSaved: (advert: Advert) => void;
};

export function CreateAdvertPage({ initialAdvert, onCancel, onSaved }: Props) {
  const [form, setForm] = useState({
    title: initialAdvert?.title ?? "",
    price: initialAdvert?.price ? String(initialAdvert.price) : "",
    description: initialAdvert?.description ?? "",
    category: initialAdvert?.category ?? "",
    location: initialAdvert?.location ?? "",
  });
  const [images, setImages] = useState<string[]>(initialAdvert?.images_paths ?? []);
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");

  const set = (key: keyof typeof form, value: string) =>
    setForm({ ...form, [key]: value });

  const onFile = async (file?: File) => {
    if (!file) return;
    try {
      setError("");
      setStatus("Загружаем фото...");
      const result = await uploadImage(file);
      setImages((current) => [...current, result.url]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Не удалось загрузить фото");
    } finally {
      setStatus("");
    }
  };

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    try {
      setError("");
      setStatus(initialAdvert ? "Сохраняем..." : "Публикуем...");
      const payload: Partial<Advert> = {
        title: form.title.trim(),
        price: Number(form.price),
        description: form.description.trim() || null,
        category: form.category.trim() || null,
        location: form.location.trim() || null,
        images_paths: images,
      };
      const saved = initialAdvert
        ? await updateAdvert(initialAdvert.id, payload)
        : await createAdvert(payload);
      onSaved(saved);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Не удалось сохранить объявление");
    } finally {
      setStatus("");
    }
  };

  return (
    <section className="form-layout">
      <div>
        <h1>{initialAdvert ? "Редактировать объявление" : "Новое объявление"}</h1>
        <p>
          Короткий заголовок, честная цена и одно хорошее фото работают лучше
          длинного текста.
        </p>
      </div>
      <form className="market-form" onSubmit={submit}>
        <input
          required
          value={form.title}
          onChange={(event) => set("title", event.target.value)}
          placeholder="Название"
        />
        <input
          required
          value={form.price}
          onChange={(event) => set("price", event.target.value)}
          inputMode="numeric"
          placeholder="Цена"
        />
        <textarea
          value={form.description}
          onChange={(event) => set("description", event.target.value)}
          placeholder="Описание"
        />
        <div className="form-grid">
          <input
            value={form.category}
            onChange={(event) => set("category", event.target.value)}
            placeholder="Категория"
          />
          <input
            value={form.location}
            onChange={(event) => set("location", event.target.value)}
            placeholder="Город"
          />
        </div>
        <label className="file-drop">
          <ImagePlus size={22} />
          <span>
            {images.length
              ? `${images.length} фото добавлено`
              : "Добавить фото"}
          </span>
          <input
            type="file"
            accept="image/png,image/jpeg,image/webp"
            onChange={(event) => onFile(event.target.files?.[0])}
          />
        </label>
        {error && <p className="error-text">{error}</p>}
        <div className="action-row">
          <button className="primary-button" disabled={Boolean(status)}>
            {status || (initialAdvert ? "Сохранить" : "Опубликовать")}
          </button>
          {onCancel && (
            <button type="button" className="secondary-button" onClick={onCancel}>
              Отмена
            </button>
          )}
        </div>
      </form>
    </section>
  );
}
