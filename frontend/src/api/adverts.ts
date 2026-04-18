import { api } from "./client";
import type { Advert, AdvertFilters } from "../types/domain";

export function getAdverts(filters: AdvertFilters, page: number) {
  const params = new URLSearchParams({
    page: String(page),
    per_page: "18",
    sort_by: filters.sortBy,
  });
  if (filters.q) params.set("q", filters.q);
  if (filters.category) params.set("category", filters.category);
  if (filters.location) params.set("location", filters.location);
  if (filters.priceMin) params.set("price_min", filters.priceMin);
  if (filters.priceMax) params.set("price_max", filters.priceMax);
  return api<Advert[]>(`/api/v1/adverts/?${params.toString()}`);
}

export function getAdvert(id: number) {
  return api<Advert>(`/api/v1/adverts/${id}`);
}

export function createAdvert(payload: Partial<Advert>) {
  return api<Advert>("/api/v1/adverts/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function toggleLike(id: number) {
  return api<{ liked: boolean; likes: number }>(`/api/v1/adverts/${id}/like`, {
    method: "POST",
  });
}

export function getFavorites() {
  return api<Advert[]>("/api/v1/users/me/favorites");
}

export async function uploadImage(file: File) {
  const form = new FormData();
  form.set("file", file);
  return api<{ url: string }>("/api/v1/uploads/images", {
    method: "POST",
    body: form,
  });
}
