# 🛒 Krist API

Бэкенд интернет-магазина одежды **Krist** на FastAPI: JWT-авторизация с access и refresh токенами, каталог товаров, корзина и заказы, профили пользователей.

**Фронтенд:** [krist-next](https://github.com/donuwave/krist-next)

Мой первый бэкенд на Python. Начинал его как учебный проект, чтобы разобраться в асинхронном FastAPI, SQLAlchemy 2.0 и миграциях, а теперь развиваю как API для фронта Krist. Конспект, который я вёл по ходу, лежит в [docs/notes.md](docs/notes.md).

![Статус](https://img.shields.io/badge/статус-в_разработке-orange?style=flat)

> [!NOTE]
> **В планах:** подключение к фронтенду [krist-next](https://github.com/donuwave/krist-next), категории и фото товаров, фильтры каталога, оформление заказа с адресом и способом оплаты, избранное, отзывы, восстановление пароля по коду из письма.

## Возможности

**Авторизация**
- Регистрация и вход, пароли хешируются через bcrypt
- JWT на асимметричных ключах (**RS256**): access-токен на 15 минут, refresh-токен на 30 дней
- Обновление access-токена по refresh-токену, эндпоинт `/me`

**Товары**
- Полный CRUD каталога, включая частичное обновление через `PATCH`

**Корзина и заказы**
- Активный заказ пользователя работает как корзина и создаётся автоматически
- Добавление и удаление товаров, изменение количества
- Подсчёт стоимости каждой позиции (цена × количество) одним SQL-запросом с подзапросом
- История заказов пользователя

**Профиль**
- Просмотр и редактирование профиля пользователя

## Технические детали

- Полностью асинхронный стек: FastAPI + SQLAlchemy 2.0 (`AsyncSession`) + asyncpg
- Модели на новом синтаксисе SQLAlchemy 2.0 (`Mapped`, `mapped_column`)
- Связи один-к-одному (пользователь ↔ профиль), один-ко-многим (пользователь → заказы) и многие-ко-многим через ассоциативную модель с доп. полями (заказ ↔ товар с количеством и ценой)
- Переиспользуемый `UserRelationMixin` для привязки моделей к пользователю
- Зависимости FastAPI (`Depends`) для сессии БД, текущего пользователя и загрузки сущностей по id
- Миграции через Alembic
- Настройки через pydantic-settings, отдельные окружения dev и prod
- Docker Compose для базы и приложения, скрипт `run.sh` поднимает БД, применяет миграции и запускает сервер

## Стек

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy_2.0-D71F00?style=flat&logo=sqlalchemy&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=flat&logo=poetry&logoColor=white)

Python, FastAPI, SQLAlchemy 2.0 (async), asyncpg, Alembic, Pydantic, PyJWT, bcrypt, PostgreSQL, Docker, Poetry

## API

Swagger доступен после запуска: [localhost:8000/docs](http://localhost:8000/docs)

| Префикс | Описание |
| --- | --- |
| `/api/v1/auth` | регистрация, вход, refresh, текущий пользователь |
| `/api/v1/product` | каталог товаров |
| `/api/v1/order` | корзина и заказы |
| `/api/v1/profile` | профили пользователей |

## Запуск

Нужны Python 3.10+, Poetry и Docker.

```bash
git clone https://github.com/donuwave/krist-fastapi.git
cd krist-fastapi
poetry install
```

Сгенерируй ключи для JWT в папку `certs/`:

```bash
mkdir certs && cd certs
openssl genrsa -out jwt-private.pem 2048
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
cd ..
```

Создай `.env.dev` по примеру `.env.example`:

```
DATABASE_URL=postgresql+asyncpg://postgres:qwerty@localhost:5436/postgres
```

Запуск поднимет Postgres в Docker, применит миграции и стартует сервер.

```bash
./run.sh        # dev
./run.sh prod   # prod, всё в Docker
```
