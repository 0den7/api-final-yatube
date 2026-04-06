# API для Yatube

Социальная сеть для публикации постов с возможностью подписываться на авторов и комментировать записи.

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:0den7/api-final-yatube.git
```
```bash
cd api-final-yatube
```
Создать и активировать виртуальное окружение:
```bash
python -m venv venv
```
```bash
. venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```
Выполнить миграции:
```bash
python manage.py migrate
```
Запустить проект:
```bash
python manage.py runserver
```

## Документация:

Когда вы запустите проект, по адресу  ```http http://127.0.0.1:8000/redoc/``` будет доступна документация для API Yatube.

## Примеры запросов:

1. Регистрация пользователя:
### Запроc:
POST ```http http://127.0.0.1:8000/api/v1/users/```
Content-Type: application/json
```json
{
    "username": "new_user",
    "password": "your_password"
}
```
### Ответ (201 Created):
```json
{
    "email": "",
    "username": "new_user",
    "id": 1
}
```

2. Получение JWT-токена:
### Запроc:
POST ```http http://127.0.0.1:8000/api/v1/jwt/create/```
Content-Type: application/json
```json
{
    "username": "new_user",
    "password": "your_password"
}
```
### Ответ (200 OK):
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

3. Создание поста:
### Запроc:
POST ```http http://127.0.0.1:8000/api/v1/posts/```
Authorization: Bearer <access_token>
Content-Type: application/json
```json
{
    "text": "Мой первый пост!",
    "group": 1
}
```
### Ответ (201 Created):
```json
{
    "id": 1,
    "author": "new_user",
    "text": "Мой первый пост!",
    "pub_date": "2026-04-06T18:46:47.299719Z",
    "image": null,
    "group": 1
}
```

## Права доступа:

Анонимные пользователи: только чтение
Аутентифицированные пользователи: создание, изменение и удаление своих постов и комментариев
Подписки доступны только аутентифицированным пользователям

## Автор:

Юрий Кудряшов
