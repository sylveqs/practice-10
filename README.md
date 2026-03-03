# Online Forum API

Backend для онлайн-форума с аутентификацией пользователей, созданием тем и обменом сообщениями. Разработан на FastAPI с использованием SQLite, JWT и SQLAlchemy.

## 📋 Содержание

- [Технологический стек](#технологический-стек)
- [Функциональность](#функциональность)
- [Установка и запуск](#установка-и-запуск)
- [Структура проекта](#структура-проекта)
- [API Эндпоинты](#api-эндпоинты)
- [Модели данных](#модели-данных)
- [Аутентификация](#аутентификация)
- [Миграции базы данных](#миграции-базы-данных)
- [Примеры запросов](#примеры-запросов)
- [Обработка ошибок](#обработка-ошибок)

## 🛠 Технологический стек

- **FastAPI** - современный веб-фреймворк для создания API
- **SQLite3** - легковесная база данных для разработки
- **SQLAlchemy** - ORM для работы с базой данных
- **JWT** - JSON Web Tokens для аутентификации
- **Alembic** - инструмент для миграций базы данных
- **Pydantic** - валидация данных и управление настройками
- **python-jose** - работа с JWT токенами
- **passlib** - хеширование паролей

## ✨ Функциональность

- ✅ Регистрация пользователей с уникальными email и username
- ✅ Аутентификация по JWT токенам (срок действия - 1 час)
- ✅ Создание и просмотр тем форума
- ✅ Добавление сообщений в темы
- ✅ Подсчет количества сообщений в теме
- ✅ Защита эндпоинтов с помощью JWT
- ✅ Валидация входных данных
- ✅ Обработка ошибок с соответствующими HTTP статусами

## 🚀 Установка и запуск

### Предварительные требования

- Python 3.8 или выше
- pip (менеджер пакетов Python)
- virtualenv (рекомендуется)

### Пошаговая установка

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/yourusername/forum-api.git
cd forum-api
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
```

3. **Активируйте виртуальное окружение:**
   - Windows:
   ```bash
   venv\Scripts\activate
   ```
   - Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

5. **Настройте переменные окружения:**
Создайте файл `.env` в корневой директории:
```env
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./forum.db
```

6. **Инициализируйте Alembic:**
```bash
alembic init alembic
```

7. **Создайте миграцию:**
```bash
alembic revision --autogenerate -m "Initial migration"
```

8. **Примените миграции:**
```bash
alembic upgrade head
```

9. **Запустите сервер:**
```bash
python run.py
```

Сервер будет доступен по адресу: `http://localhost:8000`
Документация Swagger: `http://localhost:8000/docs`
Документация ReDoc: `http://localhost:8000/redoc`

## 📁 Структура проекта

```
forum-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Главный файл приложения
│   ├── models.py                # SQLAlchemy модели
│   ├── schemas.py               # Pydantic схемы
│   ├── database.py              # Конфигурация базы данных
│   ├── auth.py                  # Функции аутентификации
│   ├── dependencies.py          # Зависимости FastAPI
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py              # Роутер аутентификации
│   │   ├── topics.py            # Роутер тем
│   │   └── posts.py             # Роутер сообщений
│   └── alembic/                  # Миграции Alembic
│       ├── versions/
│       └── env.py
├── alembic.ini                   # Конфигурация Alembic
├── requirements.txt              # Зависимости проекта
├── run.py                        # Скрипт для запуска
└── README.md                     # Документация
```

## 📚 API Эндпоинты

### Аутентификация

| Метод | Эндпоинт | Описание | Требуется JWT |
|-------|----------|----------|---------------|
| POST | `/auth/register` | Регистрация нового пользователя | Нет |
| POST | `/auth/login` | Вход в систему, получение JWT токена | Нет |
| POST | `/auth/logout` | Выход из системы | Да |

### Темы форума

| Метод | Эндпоинт | Описание | Требуется JWT |
|-------|----------|----------|---------------|
| GET | `/topics/` | Получение списка всех тем | Нет |
| POST | `/topics/` | Создание новой темы | Да |
| GET | `/topics/{topic_id}` | Получение темы и всех сообщений | Нет |

### Сообщения

| Метод | Эндпоинт | Описание | Требуется JWT |
|-------|----------|----------|---------------|
| POST | `/topics/{topic_id}/posts` | Добавление сообщения в тему | Да |

## 📊 Модели данных

### User (Пользователь)
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "created_at": "2024-01-01T12:00:00"
}
```

### Topic (Тема)
```json
{
  "id": 1,
  "title": "Заголовок темы",
  "content": "Содержание темы",
  "author_id": 1,
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

### Post (Сообщение)
```json
{
  "id": 1,
  "content": "Текст сообщения",
  "topic_id": 1,
  "author_id": 1,
  "created_at": "2024-01-01T12:00:00"
}
```

## 🔐 Аутентификация

API использует JWT (JSON Web Tokens) для аутентификации. После успешного входа вы получаете токен, который необходимо включать в заголовки последующих запросов:

```
Authorization: Bearer <your_jwt_token>
```

### Срок действия токена
- Токен действителен в течение 1 часа
- По истечении срока необходимо получить новый токен через `/auth/login`

## 🔄 Миграции базы данных

### Создание новой миграции
```bash
alembic revision --autogenerate -m "Описание изменений"
```

### Применение миграций
```bash
alembic upgrade head
```

### Откат миграции
```bash
alembic downgrade -1  # Откат на одну версию назад
alembic downgrade base  # Полный откат
```

## 📝 Примеры запросов

### Регистрация пользователя
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "john_doe",
    "password": "securepassword"
  }'
```

### Вход в систему
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

### Создание темы (требуется аутентификация)
```bash
curl -X POST "http://localhost:8000/topics/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Моя первая тема",
    "content": "Содержание моей первой темы"
  }'
```

### Добавление сообщения в тему
```bash
curl -X POST "http://localhost:8000/topics/1/posts" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Мое первое сообщение"
  }'
```

## ⚠️ Обработка ошибок

API возвращает стандартные HTTP статусы с понятными сообщениями:

| Код | Описание | Пример ответа |
|-----|----------|---------------|
| 400 | Bad Request - неверные входные данные | `{"detail": "Email or username already registered"}` |
| 401 | Unauthorized - отсутствует или невалидный JWT | `{"detail": "Invalid authentication credentials"}` |
| 404 | Not Found - ресурс не найден | `{"detail": "Topic not found"}` |
| 500 | Internal Server Error - внутренняя ошибка сервера | `{"detail": "Internal server error"}` |

## 🧪 Тестирование

### Запуск тестов
```bash
pytest
```

### Проверка покрытия кода
```bash
pytest --cov=app tests/
```

## 🔧 Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| SECRET_KEY | Секретный ключ для JWT | "your-secret-key-here-change-in-production" |
| ALGORITHM | Алгоритм шифрования JWT | "HS256" |
| ACCESS_TOKEN_EXPIRE_MINUTES | Время жизни токена (в минутах) | 60 |
| DATABASE_URL | URL подключения к БД | "sqlite:///./forum.db" |

## 📈 Производительность

- FastAPI обеспечивает высокую производительность благодаря асинхронности
- SQLite подходит для разработки, для продакшена рекомендуется PostgreSQL
- Индексы в базе данных оптимизируют поиск по email и username

<img width="1440" height="938" alt="image" src="https://github.com/user-attachments/assets/2355b13c-94cc-402e-8cac-51fba4511e97" />

<img width="1411" height="937" alt="image" src="https://github.com/user-attachments/assets/df10be7e-3dbe-4452-85a2-82aab9454b84" />

---

