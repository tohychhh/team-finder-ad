# TeamFinder

Платформа для поиска команды для pet-проектов.

## Описание

TeamFinder — это веб-приложение, которое помогает разработчикам, дизайнерам и другим специалистам находить единомышленников для совместной работы над pet-проектами. Зарегистрированные пользователи могут размещать идеи проектов, находить команду и откликаться на опубликованные предложения.

### Основные функции

- Регистрация и аутентификация пользователей
- Создание, редактирование и просмотр проектов
- Присоединение к проектам других пользователей
- Управление профилем пользователя
- Добавление навыков для проектов (Вариант 3)
- Фильтрация проектов по навыкам
- Избранное

## Технологии

- Python 3.13
- Django 5.2
- PostgreSQL (в Docker)
- Docker / Docker Compose

## Запуск проекта

1. Склонируйте репозиторий
2. Установите Docker Desktop
3. Создайте виртуальное окружение: `python -m venv venv`
4. Активируйте: `venv\Scripts\activate` (Windows)
5. Установите зависимости: `pip install -r requirements.txt`
6. Создайте файл `.env` с содержимым:
   ```env
   SECRET_KEY=django-insecure-key-for-development
   DEBUG=True
   ALLOWED_HOSTS=localhost 127.0.0.1
   DB_NAME=teamfinder
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_PORT=5432
7. Запустите PostgreSQL через Docker: `docker-compose up -d`
8. Выполните миграции: `python manage.py migrate`
9. Создайте суперпользователя: `python manage.py createsuperuser`
10. Запустите сервер: `python manage.py runserver`

## Автор

- GitHub: [tohychhh](https://github.com/tohychhh)