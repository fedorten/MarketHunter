# API Маркетплейса

В этом документе описано API для интеграции фронтенда с бэкендом.

## Базовый URL

```
http://localhost:8000
```

---

## Содержание

- [Аутентификация](#аутентификация)
  - [Регистрация](#регистрация)
  - [Вход](#вход)
- [Пользователи](#пользователи)
  - [Получение текущего пользователя](#получение-текущего-пользователя)
  - [Обновление профиля](#обновление-профиля)
- [Объявления](#объявления)
  - [Создание объявления](#создание-объявления)
  - [Получение всех объявлений](#получение-всех-объявлений)
  - [Получение одного объявления](#получение-одного-объявления)
  - [Обновление объявления](#обновление-объявления)
  - [Удаление объявления](#удаление-объявления)
- [Чаты](#чаты)
  - [Создание/получение чата](#созданиеполучение-чата)
  - [WebSocket соединение](#websocket-соединение)
- [Модели данных](#модели-данных)
- [Коды ошибок](#коды-ошибок)

---

## Аутентификация

### Регистрация

Создаёт нового пользователя.

**Endpoint:** `POST /registration`

**Request Body:**

```json
{
  "username": "Ivan",
  "phone": "+79001234567",
  "password": "securepassword123",
  "email": "ivan@example.com"
}
```

| Поле | Тип | Обязательно | Описание |
|------|-----|-------------|----------|
| username | string | Да | Имя пользователя |
| phone | string | Да | Телефон (уникальный) |
| password | string | Да | Пароль |
| email | string | Нет | Email (уникальный) |

**Response (200):**

```json
{
  "msg": "User created"
}
```

**Возможные ошибки:**
- `400` - пользователь с таким телефоном уже существует

---

### Вход

Получение токена доступа.

**Endpoint:** `POST /login`

**Content-Type:** `application/x-www-form-urlencoded`

**Request Body:**

```
username=+79001234567&password=securepassword123
```

> **Важно:** username - это телефон пользователя

**Response (200):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Использование токена:**

Для защищённых endpoints токен передаётся в заголовке:

```
Authorization: Bearer <access_token>
```

**Время жизни токена:** 30 минут

---

## Пользователи

### Получение текущего пользователя

Возвращает данные авторизованного пользователя.

**Endpoint:** `GET /api/v1/users/me`

**Headers:** `Authorization: Bearer <token>`

**Response (200):**

```json
{
  "username": "Ivan",
  "phone": "+79001234567",
  "email": "ivan@example.com"
}
```

---

### Обновление профиля

Обновляет данные текущего пользователя.

**Endpoint:** `PATCH /api/v1/users/me`

**Headers:** `Authorization: Bearer <token>`

**Request Body (все поля опциональны):**

```json
{
  "username": "Ivan Ivanov",
  "email": "newemail@example.com"
}
```

> **Примечание:** Чтобы изменить пароль, передайте поле `password` с новым паролем.

**Response (200):**

```json
{
  "username": "Ivan Ivanov",
  "phone": "+79001234567",
  "email": "newemail@example.com"
}
```

---

## Объявления

### Создание объявления

Создаёт новое объявление от имени текущего пользователя.

**Endpoint:** `POST /api/v1/adverts`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**

```json
{
  "title": "iPhone 15 Pro",
  "price": 85000,
  "description": "Отличное состояние, полный комплект",
  "category": "electronics",
  "images_paths": "['/img/1.jpg', '/img/2.jpg']",
  "location": "Москва",
  "owner_id": 1
}
```

| Поле | Тип | Обязательно | Описание |
|------|-----|-------------|----------|
| title | string | Да | Заголовок объявления |
| price | integer | Да | Цена в рублях |
| description | string | Нет | Описание |
| category | string | Нет | Категория |
| images_paths | string | Нет | JSON массив путей к изображениям |
| location | string | Нет | Местоположение |
| owner_id | integer | Да | ID владельца (должен совпадать с текущим пользователем) |

**Response (200):**

```json
{
  "title": "iPhone 15 Pro",
  "price": 85000,
  "description": "Отличное состояние, полный комплект",
  "category": "electronics",
  "images_paths": "['/img/1.jpg', '/img/2.jpg']",
  "location": "Москва"
}
```

---

### Получение всех объявлений

Возвращает список всех объявлений.

**Endpoint:** `GET /api/v1/adverts`

**Response (200):**

```json
[
  {
    "title": "iPhone 15 Pro",
    "price": 85000,
    "description": "Отличное состояние",
    "category": "electronics",
    "images_paths": "['/img/1.jpg']",
    "location": "Москва"
  },
  {
    "title": "Диван",
    "price": 15000,
    "description": "Б/у",
    "category": "furniture",
    "images_paths": null,
    "location": "СПб"
  }
]
```

> **Примечание:** В текущей версии возвращаются все объявления. Пагинация не реализована.

---

### Получение одного объявления

Возвращает данные конкретного объявления.

**Endpoint:** `GET /api/v1/adverts/{id}`

**Response (200):**

```json
{
  "title": "iPhone 15 Pro",
  "price": 85000,
  "description": "Отличное состояние",
  "category": "electronics",
  "images_paths": "['/img/1.jpg']",
  "location": "Москва"
}
```

**Возможные ошибки:**
- `404` - объявление не найдено

---

### Обновление объявления

Обновляет данные объявления (только для владельца).

**Endpoint:** `PATCH /api/v1/adverts/{id}`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**

```json
{
  "price": 80000
}
```

**Response (200):**

```json
{
  "title": "iPhone 15 Pro",
  "price": 80000,
  "description": "Отличное состояние",
  "category": "electronics",
  "images_paths": "['/img/1.jpg']",
  "location": "Москва"
}
```

**Возможные ошибки:**
- `401` - вы не владелец этого объявления
- `404` - объявление не найдено

---

### Удаление объявления

Удаляет объявление (только для владельца).

**Endpoint:** `DELETE /api/v1/adverts/{id}`

**Headers:** `Authorization: Bearer <token>`

**Response (200):**

```json
{
  "title": "iPhone 15 Pro",
  "price": 85000,
  ...
}
```

**Возможные ошибки:**
- `401` - вы не владелец этого объявления
- `404` - объявление не найдено

---

## Чаты

### Создание/получение чата

Создаёт новый чат или возвращает существующий по объявлению.

**Endpoint:** `POST /api/v1/chats/{advert_id}`

**Headers:** `Authorization: Bearer <token>`

**Response (200):**

```json
{
  "chat_id": 1,
  "is_new": true
}
```

| Поле | Тип | Описание |
|------|-----|----------|
| chat_id | integer | ID чата |
| is_new | boolean | true - создан новый чат, false - получен существующий |

**Возможные ошибки:**
- `404` - объявление не найдено
- `404` - нельзя написать владельцу своего объявления

---

### WebSocket соединение

Подключение к чату для обмена сообщениями в реальном времени.

**URL:** `ws://localhost:8000/api/v1/chats/ws/{chat_id}?token=<access_token>`

**Query Parameters:**

| Параметр | Тип | Обязательно | Описание |
|----------|-----|-------------|----------|
| chat_id | integer | Да | ID чата |
| token | string | Да | JWT токен доступа |

**Пример подключения (JavaScript):**

```javascript
const token = localStorage.getItem('access_token');
const chatId = 1;
const ws = new WebSocket(`ws://localhost:8000/api/v1/chats/ws/${chatId}?token=${token}`);

ws.onopen = () => {
  console.log('Подключено к чату');
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Новое сообщение:', message);
  // message содержит: { id, chat_id, sender_id, content, is_read, create_date }
};

ws.onclose = () => {
  console.log('Отключено от чата');
};

ws.onerror = (error) => {
  console.error('Ошибка:', error);
};

// Отправка сообщения
ws.send('Привет!');

// Закрытие соединения
ws.close();
```

**Формат сообщения (входящие и исходящие):**

```json
{
  "id": 1,
  "chat_id": 1,
  "sender_id": 2,
  "content": "Привет!",
  "is_read": false,
  "create_date": "2024-01-15T10:30:00"
}
```

**Правила доступа:**
- Отправить сообщение может только участник чата (покупатель или владелец объявления)

---

## Модели данных

### User (Пользователь)

```json
{
  "username": "string",
  "phone": "string",
  "email": "string | null"
}
```

### Advert (Объявление)

```json
{
  "title": "string",
  "price": "integer",
  "description": "string | null",
  "category": "string | null",
  "images_paths": "string | null",
  "location": "string | null"
}
```

### Chat (Чат)

```json
{
  "chat_id": "integer",
  "is_new": "boolean"
}
```

### Message (Сообщение)

```json
{
  "id": "integer",
  "chat_id": "integer",
  "sender_id": "integer",
  "content": "string",
  "is_read": "boolean",
  "create_date": "datetime (ISO 8601)"
}
```

---

## Коды ошибок

| Код | Описание |
|-----|----------|
| 400 | Некорректный запрос (неверные данные) |
| 401 | Не авторизован (неверный токен) |
| 404 | Ресурс не найден |
| 422 | Ошибка валидации данных |

**Пример ответа с ошибкой:**

```json
{
  "detail": "User with this phone already exists"
}
```

---

## Быстрый старт для фронтенда

### 1. Регистрация пользователя

```javascript
async function register(username, phone, password, email) {
  const response = await fetch('http://localhost:8000/registration', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, phone, password, email })
  });
  return response.json();
}
```

### 2. Вход и сохранение токена

```javascript
async function login(phone, password) {
  const formData = new URLSearchParams();
  formData.append('username', phone);
  formData.append('password', password);
  
  const response = await fetch('http://localhost:8000/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData
  });
  
  const data = await response.json();
  localStorage.setItem('access_token', data.access_token);
  return data;
}

// Удобная функция для получения заголовков
function getAuthHeaders() {
  const token = localStorage.getItem('access_token');
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  };
}
```

### 3. Получение списка объявлений

```javascript
async function getAdverts() {
  const response = await fetch('http://localhost:8000/api/v1/adverts/');
  return response.json();
}
```

### 4. Создание объявления

```javascript
async function createAdvert(title, price, description) {
  const response = await fetch('http://localhost:8000/api/v1/adverts/', {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({
      title,
      price,
      description,
      owner_id: 1  // ID текущего пользователя
    })
  });
  return response.json();
}
```

### 5. Подключение к чату

```javascript
function connectToChat(chatId) {
  const token = localStorage.getItem('access_token');
  return new WebSocket(`ws://localhost:8000/api/v1/chats/ws/${chatId}?token=${token}`);
}
```

---

## Особенности реализации

1. **Токен** - JWT токен, истекает через 30 минут
2. **Аутентификация** - по телефону и паролю (OAuth2 Password Flow)
3. **База данных** - SQLite (файл `marketplace.db`)
4. **Админ-панель** - доступна по адресу `/admin` (только для администраторов)

---

## Контакты для связи

При возникновении вопросов по API обращаться к backend-разработчику.
