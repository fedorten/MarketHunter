import { ImagePlus } from 'lucide-react'
import { FormEvent, useState } from 'react'
import { createAdvert, uploadImage } from '../api/adverts'
import type { Advert } from '../types/domain'

type Props = {
  onCreated: (id: number) => void
}

export function CreateAdvertPage({ onCreated }: Props) {
  const [form, setForm] = useState({ title: '', price: '', description: '', category: '', location: '' })
  const [images, setImages] = useState<string[]>([])
  const [status, setStatus] = useState('')

  const set = (key: keyof typeof form, value: string) => setForm({ ...form, [key]: value })

  const onFile = async (file?: File) => {
    if (!file) return
    setStatus('Загружаем фото...')
    const result = await uploadImage(file)
    setImages((current) => [...current, result.url])
    setStatus('')
  }

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    setStatus('Публикуем...')
    const payload: Partial<Advert> = {
      title: form.title,
      price: Number(form.price),
      description: form.description,
      category: form.category,
      location: form.location,
      images_paths: images,
    }
    const created = await createAdvert(payload)
    onCreated(created.id)
  }

  return (
    <section className="form-layout">
      <div>
        <h1>Новое объявление</h1>
        <p>Короткий заголовок, честная цена и одно хорошее фото работают лучше длинного текста.</p>
      </div>
      <form className="market-form" onSubmit={submit}>
        <input required value={form.title} onChange={(event) => set('title', event.target.value)} placeholder="Название" />
        <input required value={form.price} onChange={(event) => set('price', event.target.value)} inputMode="numeric" placeholder="Цена" />
        <textarea value={form.description} onChange={(event) => set('description', event.target.value)} placeholder="Описание" />
        <div className="form-grid">
          <input value={form.category} onChange={(event) => set('category', event.target.value)} placeholder="Категория" />
          <input value={form.location} onChange={(event) => set('location', event.target.value)} placeholder="Город" />
        </div>
        <label className="file-drop">
          <ImagePlus size={22} />
          <span>{images.length ? `${images.length} фото добавлено` : 'Добавить фото'}</span>
          <input type="file" accept="image/png,image/jpeg,image/webp" onChange={(event) => onFile(event.target.files?.[0])} />
        </label>
        <button className="primary-button" disabled={Boolean(status)}>{status || 'Опубликовать'}</button>
      </form>
    </section>
  )
}
