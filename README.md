# API YaMDb

Проект API YaMDb представляет собой возможность пользователей оставлять отзывы на произведения.
Ниже приведены основные возможности API YaMDb:

- Получение подробной информации о произведениях, включая название, описание, рейтинг, категории и жанры.
- Добавление отзывов и комментариев к произведениям.
- Получение информации о категориях произведений.
- Получение информации о жанрах произведений.
- Роли пользователей, определяющие их права доступа (Superuser Django, администратор, модератор, аутентифицированный пользователь, аноним).

### Авторы:
- [Корсаков Сергей](https://github.com/mortodello)
- [Земцова Елизавета](https://github.com/Elizaveta-u)
- [Демков Борис](https://github.com/AIofHuman)

## Использованные технологии

API YaMDB разработан с использованием следующих технологий:

- Python - язык программирования, на котором написано API.
- Django - фреймворк, используемый для разработки веб-приложений на Python.
- Django REST framework - библиотека, расширяющая возможности Django для создания REST API.

API YaMDB использует функциональность Django и Django REST framework для реализации CRUD операций (создание, чтение, обновление, удаление) с данными произведения, отзывов, комментариев, категорий и жанров. Также API использует систему прав доступа, позволяющую ограничивать доступ к определенным функциям в зависимости от роли пользователя.

### Как запустить проект:

1. Клонируйте репозиторий и перейдите в папку проекта:

```bash
git clone https://github.com/mortodello/api_yamdb.git
cd api_yamdb
```

2. Создайте и активируйте виртуальное окружение:

```
python -m venv venv
source venv/bin/activate
```

3. Установите зависимости:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Выполните миграции:

```
python manage.py migrate
```

5. Создайте суперпользователя:

```
python manage.py createsuperuser
```

6. Заполните базу данных тестовой информацией:

```
python manage.py database_loading
```

7. Запустите сервер:

```
python manage.py runserver
```

### Примеры запросов и ответов:

1. Регистрация пользователя:
   - Запрос: POST /api/v1/auth/signup/
   - Тело запроса:
   ```
    {
        "email": "user@example.com",
        "username": "string"
    }   
   ```
   - Ответ: 200 
   ```
    {
        "email": "string",
        "username": "string"
    }
   ```

2. Получение пользователя по имени пользователя:
   - Запрос: GET /api/v1 /users/{имя пользователя}/

   - Ответ: 200 
   ```
    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }
   ```

3. Получение списка всех комментариев к отзыву:
   - Запрос: GET /api/v1 /titles/{title_id}/reviews/{review_id}/comments/

   - Ответ: 200 
   ```
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
            "id": 0,
            "text": "string",
            "author": "string",
            "pub_date": "2019-08-24T14:15:22Z"
            }
        ]
    }
   ```

4. Добавление нового отзыва:
   - Запрос: POST /api/v1 /titles/{title_id}/reviews/
   - Тело запроса:
   ```
    { 
        "text": "string",
        "score": 1
    }   
   ```
   - Ответ: 201 
   ```
    {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
    }
   ```

5. Получение списка всех жанров:
   - Запрос: GET /api/v1/genres/
   - Ответ: 200 OK
   ```
   {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
            "name": "string",
            "slug": "string"
            }
        ]
}
   ```
