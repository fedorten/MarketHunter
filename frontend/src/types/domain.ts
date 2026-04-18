export type Advert = {
  id: number;
  title: string;
  price: number;
  description?: string | null;
  category?: string | null;
  images_paths?: string[] | null;
  location?: string | null;
  views?: number;
  likes?: number;
  owner_id: number;
  create_date?: string;
};

export type User = {
  id: number;
  username: string;
  phone: string;
  email?: string | null;
};

export type Message = {
  id: number;
  chat_id: number;
  sender_id: number;
  content: string;
  is_read: boolean;
  create_date: string;
};

export type Chat = {
  id: number;
  advert_id: number;
  advert_title: string;
  advert_price: number;
  advert_image?: string | null;
  buyer_id: number;
  seller_id: number;
  companion: {
    id: number;
    username: string;
  };
  last_message?: Message | null;
  unread_count: number;
};

export type AdvertFilters = {
  q: string;
  category: string;
  location: string;
  priceMin: string;
  priceMax: string;
  sortBy: string;
};
