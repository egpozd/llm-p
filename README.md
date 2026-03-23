# llm-p

Backend-сервис на **FastAPI** с **JWT-аутентификацией**, хранением данных в **SQLite** и интеграцией с **OpenRouter** для работы с LLM.

## Описание проекта

В рамках задания разработан backend-сервис на языке Python с использованием фреймворка FastAPI.

В проекте реализованы:

- регистрация пользователя;
- вход пользователя и получение JWT access token;
- получение данных текущего пользователя;
- отправка запроса в LLM через OpenRouter;
- сохранение истории сообщений пользователя в базе данных SQLite;
- просмотр истории сообщений;
- очистка истории сообщений.

## Функциональные возможности

Сервис предоставляет следующие API-методы:

- `POST /auth/register` — регистрация нового пользователя;
- `POST /auth/login` — вход пользователя и получение access token;
- `GET /auth/me` — получение информации о текущем пользователе;
- `POST /chat` — отправка сообщения в LLM;
- `GET /chat/history` — просмотр истории сообщений;
- `DELETE /chat/history` — очистка истории сообщений;
- `GET /health` — проверка состояния сервиса.

## Используемые технологии

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy 2.0
- SQLite
- Pydantic
- pydantic-settings
- python-jose
- passlib
- bcrypt
- httpx
- OpenRouter API
- Ruff

## Архитектура проекта

Проект разделён на несколько слоёв:

- `api` — HTTP-роуты и зависимости FastAPI;
- `schemas` — Pydantic-схемы запросов и ответов;
- `repositories` — слой работы с базой данных;
- `services` — внешние сервисы, включая OpenRouter client;
- `usecases` — бизнес-логика приложения;
- `db` — база, сессии и ORM-модели;
- `core` — настройки, безопасность и доменные ошибки.

Такое разделение позволяет не смешивать HTTP-слой, бизнес-логику и работу с хранилищем данных.

## Структура проекта

```text
llm-p/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   ├── routes_auth.py
│   │   └── routes_chat.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── errors.py
│   │   └── security.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── models.py
│   │   └── session.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── chat_messages.py
│   │   └── users.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── chat.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── openrouter_client.py
│   ├── usecases/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── chat.py
│   ├── __init__.py
│   └── main.py
├── .env
├── .env.example
├── app.db
├── pyproject.toml
└── README.md
```

## Установка и запуск

### 1. Создание проекта и переход в каталог

```powershell
mkdir llm-p
cd llm-p
```

### 2. Создание виртуального окружения

```powershell
uv venv
.\.venv\Scripts\Activate.ps1
```

### 3. Установка зависимостей

```powershell
uv sync
```

## Настройка переменных окружения

Создайте файл `.env` на основе `.env.example`.

Пример содержимого `.env`:

```env
APP_NAME=llm-p
ENV=local

JWT_SECRET=my_super_secret_key_123456789
JWT_ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

SQLITE_PATH=./app.db

OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=stepfun/step-3.5-flash:free
OPENROUTER_SITE_URL=https://example.com
OPENROUTER_APP_NAME=llm-fastapi-openrouter
```

## Запуск приложения

Для запуска сервера используйте команду:

```powershell
uv run uvicorn app.main:app --reload --port 8000
```

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:8000
```

Интерактивная документация Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Описание основных API-методов

### Регистрация пользователя

**Endpoint:**

```http
POST /auth/register
```

**Пример запроса:**

```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

**Пример ответа:**

```json
{
  "id": 1,
  "email": "test@example.com",
  "role": "user"
}
```

### Вход пользователя

**Endpoint:**

```http
POST /auth/login
```

В Swagger форма входа использует:

- `username` — email пользователя;
- `password` — пароль.

**Пример ответа:**

```json
{
  "access_token": "jwt_token_value",
  "token_type": "bearer"
}
```

### Получение текущего пользователя

**Endpoint:**

```http
GET /auth/me
```

**Пример ответа:**

```json
{
  "id": 1,
  "email": "test@example.com",
  "role": "user"
}
```

### Отправка сообщения в LLM

**Endpoint:**

```http
POST /chat
```

**Пример запроса:**

```json
{
  "prompt": "Привет! Очень коротко объясни, что такое FastAPI.",
  "system": "Отвечай очень просто и в 2-3 предложениях.",
  "max_history": 10,
  "temperature": 0.7
}
```

**Пример ответа:**

```json
{
  "answer": "FastAPI — это современный Python-фреймворк для создания API. Он быстрый, удобный и автоматически создает документацию."
}
```

### Просмотр истории сообщений

**Endpoint:**

```http
GET /chat/history
```

**Пример ответа:**

```json
[
  {
    "id": 1,
    "role": "user",
    "content": "Привет! Очень коротко объясни, что такое FastAPI.",
    "created_at": "2026-03-23T20:00:00"
  },
  {
    "id": 2,
    "role": "assistant",
    "content": "FastAPI — это современный Python-фреймворк для создания API.",
    "created_at": "2026-03-23T20:00:03"
  }
]
```

### Очистка истории сообщений

**Endpoint:**

```http
DELETE /chat/history
```

**Пример ответа:**

```json
{
  "status": "ok"
}
```

### Проверка состояния приложения

**Endpoint:**

```http
GET /health
```

**Пример ответа:**

```json
{
  "status": "ok",
  "environment": "local"
}
```

## Логика работы приложения

1. Пользователь регистрируется через `/auth/register`.
2. Пользователь входит в систему через `/auth/login`.
3. После авторизации пользователь может вызывать защищённые методы.
4. Запрос в `/chat` отправляется в OpenRouter.
5. Ответ модели сохраняется в SQLite вместе с сообщением пользователя.
6. История сообщений доступна через `/chat/history`.
7. История может быть очищена через `DELETE /chat/history`.

## Безопасность

В проекте реализованы следующие меры безопасности:

- пароли пользователей не хранятся в открытом виде, а хешируются;
- для авторизации используется JWT;
- защищённые endpoint’ы доступны только после успешной аутентификации;
- история сообщений хранится отдельно для каждого пользователя.

## База данных

В проекте используется SQLite.
Файл базы данных создаётся автоматически при запуске приложения.

### Основные таблицы

- `users`
- `chat_messages`

### Таблица `users`

Содержит:

- идентификатор пользователя;
- email;
- хеш пароля;
- роль пользователя;
- дату создания записи.

### Таблица `chat_messages`

Содержит:

- идентификатор сообщения;
- идентификатор пользователя;
- роль сообщения (`user` или `assistant`);
- текст сообщения;
- дату и время создания.

## Проверка проекта

Проверка выполнялась через Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Последовательность проверки:

1. выполнить `POST /auth/register`;
2. выполнить `POST /auth/login`;
3. авторизоваться в Swagger;
4. проверить `GET /auth/me`;
5. выполнить `POST /chat`;
6. проверить `GET /chat/history`;
7. выполнить `DELETE /chat/history`;
8. повторно проверить `GET /chat/history`.

## Линтинг

Для проверки качества кода используется Ruff.

Команда запуска:

```powershell
uv run ruff check .
```

Результат проверки:

```text
All checks passed!
```

## Итог

В результате выполнения задания разработан backend-сервис на FastAPI с JWT-аутентификацией, хранением данных в SQLite и интеграцией с OpenRouter. Реализованы регистрация, вход, получение профиля, отправка запросов в LLM, просмотр и очистка истории сообщений. Работоспособность проекта подтверждена тестированием через Swagger UI и проверкой линтером Ruff.
