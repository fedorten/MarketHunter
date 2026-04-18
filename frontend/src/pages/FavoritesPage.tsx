import { useEffect, useState } from 'react'
import { getFavorites } from '../api/adverts'
import { AdvertCard } from '../components/AdvertCard'
import { EmptyState } from '../components/EmptyState'
import type { Advert } from '../types/domain'

type Props = {
  onOpenAdvert: (id: number) => void
}

export function FavoritesPage({ onOpenAdvert }: Props) {
  const [items, setItems] = useState<Advert[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getFavorites().then(setItems).finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="load-marker">Загружаем избранное...</div>

  return (
    <>
      <section className="section-head">
        <h1>Избранное</h1>
        <p>Все объявления, к которым хочется вернуться.</p>
      </section>
      {items.length === 0 ? (
        <EmptyState title="Пока пусто" text="Отмечайте объявления сердцем в ленте." />
      ) : (
        <div className="adverts-grid">
          {items.map((advert, index) => (
            <AdvertCard key={advert.id} advert={advert} index={index} onOpen={onOpenAdvert} />
          ))}
        </div>
      )}
    </>
  )
}
