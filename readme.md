# TeamFinder

Платформа для поиска команды для pet-проектов.

## Технологии

- Python 3.13
- Django 5.2
- SQLite

## Запуск проекта

1. Склонируйте репозиторий
2. Создайте виртуальное окружение: `python -m venv venv`
3. Активируйте: `venv\Scripts\activate` (Windows)
4. Установите зависимости: `pip install -r requirements.txt`
5. Создайте файл `.env` с содержимым:
SECRET_KEY=django-insecure-key-for-development
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1
6. Выполните миграции: `python manage.py migrate`
7. Создайте суперпользователя: `python manage.py createsuperuser`
8. Запустите сервер: `python manage.py runserver`

## Автор

- GitHub: [tohychhh](https://github.com/tohychhh)