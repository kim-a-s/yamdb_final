# Проект api_yamdb

![Yamdb](https://github.com/kim-a-s/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# Описание проекта:

Бэкенд учебного группового проекта YaMDb для взаимодействия по API.  
Проект собирает отзывы пользователей на произведения (книги, фильмы, музыка). Возможности:
* Загрузка базы проекта из внешних файлов (csv).
* Регистрация пользователей с подтверждением через e-mail.
* Разграничение прав пользователей - администратор, модератор и пользователь.
* Зарегистрированные пользователи могут оставлять отзывы с оценкой произведения, а также комментарии к отзывам.
* Формирование рейтинга произведений по оценкам пользователей.

После локального запуска проекта полную документацию API с примерами можно найти по ссылке:  
<http://localhost/redoc/>


## Описание команд для локального запуска приложения в контейнерах

 Клонируйте проект себе

```bash
  git clone https://link-to-project
```

Перейдите в корневую папку проекта

```bash
  cd my-project
```

Перейдите в папку infra, содержащую файл docker-compose.yaml

```bash
  cd infra
```

Разверните проект в контейнерах

```bash
  docker-compose up -d
```

Выполните миграции

```bash
  docker-compose exec web python3 manage.py migrate
```

Загрузите статику

```bash
  docker-compose exec web python3 manage.py collectstatic --no-input
```

Создайте суперпользователя

```bash
  docker-compose exec web python3 manage.py createsuperuser
```


# Примеры запросов:
 
 ## Регистрация нового пользователя


```
POST /api/v1/auth/signup/
```
Параметры тела запроса:
| Имя     | Тип       | Описание                           |
|---------|-----------|------------------------------------|
| username | string | Имя пользователя |
| email | string \<email> | Email |

Пример успешного ответа:
```
{
  "email": "string",
  "username": "string"
}
```
## Получение JWT-токена
```
POST /api/v1/auth/token/
```
Параметры тела запроса:
| Имя     | Тип       | Описание                           |
|---------|-----------|------------------------------------|
| username | string | Имя пользователя |
| confirmation_code | string | Код подтверждения |

Пример успешного ответа:
```
{
"token": "string"
}
```

## Получение списка всех произведений
```
GET /api/v1/titles/
```

Параметры запроса:
| Имя     | Тип       | Описание                           |
|---------|-----------|------------------------------------|
| category | string | **опционально** <p> Категория </p>|
| genre | string | **опционально** <p> Жанр </p>|
| name | string | **опционально** <p> Название произведения </p>|
| year | integer | **опционально** <p> Год выпуска </p>|

Пример успешного ответа:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```

## Добавление нового отзыва
```
POST /api/v1/{title_id}/reviews/
```
Параметры запроса
| Имя     | Тип       | Описание                           |
|---------|-----------|------------------------------------|
| title_id | integer | ID произведения|

Параметры тела запроса:
| Имя     | Тип       | Описание                           |
|---------|-----------|------------------------------------|
| text | string | Текст отзыва|
| score | integer [1..10] | Оценка |

Пример успешного ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

## Получение комментария к отзыву
``` 
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
Параметры запроса
| Имя     | Тип       | Описание                           |
|---------|-----------|------------------------------------|
| title_id | integer | ID произведения|
| review_id | integer | ID отзыва|
| comment_id | integer | ID комментария|


Пример успешного ответа:
```
{
"id": 0,
"text": "string",
"author": "string",
"pub_date": "2019-08-24T14:15:22Z"
}
```

## Шаблон наполнения env-файла
```bash
DB_NAME=postgres
```

## Ссылка на локально развернутый проект
http://localhost/admin/

## Ccылка на развернутый проект на сервере
http://158.160.48.191/admin/

# Использованные технологии:

* [python](https://www.python.org/doc/)
* [django](https://docs.djangoproject.com/en/3.2/)
* [django-rest-framework](https://www.django-rest-framework.org/)
* [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
* Docker-compose 3.8
* nginx 1.21.3-alpine
* PostgresSQL

# Авторы:

* [Мамед Алибеков](https://github.com/Niechec) (Регистрация и аутентификация, пользователи)
* [Вадим Гуржий](https://github.com/VadimGurzhy) (Произведения, категории, жанры, импорт данных из csv)
* [Алексей Ким](https://github.com/kim-a-s) (Отзывы, комментарии, рейтинги)