import { Search, SlidersHorizontal } from "lucide-react";
import type { AdvertFilters } from "../types/domain";

type Props = {
  filters: AdvertFilters;
  onChange: (filters: AdvertFilters) => void;
  onSubmit: () => void;
};

export function SearchFilters({ filters, onChange, onSubmit }: Props) {
  const set = (key: keyof AdvertFilters, value: string) => {
    onChange({ ...filters, [key]: value });
  };

  return (
    <section className="search-band">
      <div className="search-main">
        <Search size={21} />
        <input
          value={filters.q}
          onChange={(event) => set("q", event.target.value)}
          onKeyDown={(event) => event.key === "Enter" && onSubmit()}
          placeholder="Что ищем?"
        />
        <button onClick={onSubmit}>Найти</button>
      </div>

      <div className="filters-row">
        <label>
          <SlidersHorizontal size={17} />
          <select
            value={filters.category}
            onChange={(event) => set("category", event.target.value)}
          >
            <option value="">Все категории</option>
            <option value="electronics">Электроника</option>
            <option value="transport">Транспорт</option>
            <option value="home">Дом</option>
            <option value="clothes">Одежда</option>
          </select>
        </label>
        <input
          value={filters.location}
          onChange={(event) => set("location", event.target.value)}
          placeholder="Город"
        />
        <input
          value={filters.priceMin}
          onChange={(event) => set("priceMin", event.target.value)}
          inputMode="numeric"
          placeholder="Цена от"
        />
        <input
          value={filters.priceMax}
          onChange={(event) => set("priceMax", event.target.value)}
          inputMode="numeric"
          placeholder="до"
        />
        <select
          value={filters.sortBy}
          onChange={(event) => set("sortBy", event.target.value)}
        >
          <option value="popular">Популярные</option>
          <option value="latest">Новые</option>
          <option value="price">По цене</option>
        </select>
      </div>
    </section>
  );
}
