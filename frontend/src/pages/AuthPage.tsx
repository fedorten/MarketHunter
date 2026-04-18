import { FormEvent, useState } from 'react'
import { login, register } from '../api/auth'
import type { User } from '../types/domain'

type Props = {
  onLogin: (user?: User) => void
}

export function AuthPage({ onLogin }: Props) {
  const [isRegister, setIsRegister] = useState(false)
  const [form, setForm] = useState({ username: '', phone: '', email: '', password: '' })
  const [error, setError] = useState('')

  const set = (key: keyof typeof form, value: string) => setForm({ ...form, [key]: value })

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    setError('')
    try {
      if (isRegister) await register(form)
      await login(form.phone, form.password)
      onLogin()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Не получилось войти')
    }
  }

  return (
    <section className="auth-layout">
      <div>
        <h1>{isRegister ? 'Создать профиль' : 'Войти в Круг'}</h1>
        <p>Покупки, избранное и сообщения хранятся в вашем профиле.</p>
      </div>
      <form className="market-form" onSubmit={submit}>
        {isRegister && (
          <>
            <input required value={form.username} onChange={(event) => set('username', event.target.value)} placeholder="Имя" />
            <input value={form.email} onChange={(event) => set('email', event.target.value)} placeholder="Email" />
          </>
        )}
        <input required value={form.phone} onChange={(event) => set('phone', event.target.value)} placeholder="Телефон" />
        <input required value={form.password} onChange={(event) => set('password', event.target.value)} type="password" placeholder="Пароль" />
        {error && <p className="error-text">{error}</p>}
        <button className="primary-button">{isRegister ? 'Зарегистрироваться' : 'Войти'}</button>
        <button className="text-button" type="button" onClick={() => setIsRegister(!isRegister)}>
          {isRegister ? 'Уже есть аккаунт' : 'Создать аккаунт'}
        </button>
      </form>
    </section>
  )
}
