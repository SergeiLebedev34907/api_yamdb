# api_yamdb

## Проект YaMDb
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

## Пользовательские роли
Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

## Для взаимодействия с ресурсами настроены следующие эндпоинты:
- api/v1/auth/signup/ (POST): регистрация нового пользователя.
- api/v1/auth/token/ (POST): получение JWT-токена.
- api/v1/categories/ (GET, POST): получить список всех категорий, создать категорию.
- api/v1/categories/{slug}/ (DELETE): удалить категорию.
- api/v1/genres/ (GET, POST): получить список всех жанров, создать жанр.
- api/v1/genres/{slug}/ (DELETE): удалить жанр.
- api/v1/titles/ (GET, POST): получить список всех объектов, добавить новое произведение.
- api/v1/titles/{title_id}/ (GET, PATCH, DELETE): получить информацию о произведении, обновить информацию о произведении, удалить произведение.
- api/v1/titles/{title_id}/reviews/ (GET, POST): получить список всех отзывов, добавить новый отзыв.
- api/v1/titles/{title_id}/reviews/{review_id}/ (GET, PATCH, DELETE): получить отзыв по id для указанного произведения, частично обновить отзыв по id, удалить отзыв по id.
- api/v1/titles/{title_id}/reviews/{review_id}/comments/ (GET, POST): получить список всех комментариев к отзыву по id, добавить новый комментарий для отзыва.
- api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ (GET, PATCH, DELETE): получить комментарий для отзыва по id, частично обновить комментарий к отзыву по id, удалить комментарий к отзыву по id.
- api/v1/users/ (GET, POST): получить список всех пользователей, добавить нового пользователя.
- api/v1/users/{username}/ (GET, PATCH, DELETE): получить пользователя по username, изменить данные пользователя по username, удалить пользователя по username.

## Примеры запросов

### Пример POST-запроса: регистрация нового пользователя.

POST ...api/v1/auth/signup/
```sh
{
  "email": "string",
  "username": "string"
}
```
Пример ответа:
```sh
{
  "email": "string",
  "username": "string"
}
```

### Пример POST-запроса: получение JWT-токена.

POST ...api/v1/auth/token/
```sh
{
  "username": "string",
  "confirmation_code": "string"
}
```
Пример ответа:
```sh
{
  "token": "string"
}
```

### Пример GET-запроса: получить список всех категорий.

GET ...api/v1/categories/

Пример ответа:
```sh
[
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
]
```

### Пример POST-запроса: создать категорию.

POST ...api/v1/categories/
```sh
{
  "name": "string",
  "slug": "string"
}
```
Пример ответа:
```sh
{
  "name": "string",
  "slug": "string"
}
```

### Пример GET-запроса: получить список всех жанров.

GET ...api/v1/genres/

Пример ответа:
```sh
[
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
]
```

### Пример POST-запроса: создать жанр.

POST ...api/v1/genres/
```sh
{
  "name": "string",
  "slug": "string"
}
```

### Пример GET-запроса: получить список всех объектов.

GET ...api/v1/titles/

Пример ответа:
```sh
[
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
]
```

### Пример POST-запроса: добавить новое произведение.

POST ...api/v1/titles/
```sh
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Пример ответа:
```sh
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
```

### Пример GET-запроса: получить информацию о произведении.

GET ...api/v1/titles/{title_id}/

Пример ответа:
```sh
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
```

### Пример PATCH-запроса: обновить информацию о произведении.

PATCH ...api/v1/titles/{title_id}/
```sh
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Пример ответа:
```sh
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
```

### Пример GET-запроса: получить список всех отзывов.

GET ...api/v1/titles/{title_id}/reviews/

Пример ответа:
```sh
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```

### Пример POST-запроса: добавить новый отзыв.

POST ...api/v1/titles/{title_id}/reviews/
```sh
{
  "text": "string",
  "score": 1
}
```
Пример ответа:
```sh
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### Пример GET-запроса: получить отзыв по id для указанного произведения.

GET ...api/v1/titles/{title_id}/reviews/{review_id}/

Пример ответа:
```sh
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### Пример PATCH-запроса: частично обновить отзыв по id.

PATCH ...api/v1/titles/{title_id}/reviews/{review_id}/
```sh
{
  "text": "string",
  "score": 1
}
```
Пример ответа:
```sh
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### Пример GET-запроса: получить список всех комментариев к отзыву по id.

GET ...api/v1/titles/{title_id}/reviews/{review_id}/comments/
Пример ответа:
```sh
[
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
]
```

### Пример POST-запроса: добавить новый комментарий для отзыва.

POST ...api/v1/titles/{title_id}/reviews/{review_id}/comments/
```sh
{
  "text": "string"
}
```
Пример ответа:
```sh
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### Пример GET-запроса: получить комментарий для отзыва по id.

GET ...api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

Пример ответа:
```sh
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### Пример PATCH-запроса: частично обновить комментарий к отзыву по id.

PATCH ...api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```sh
{
  "text": "string"
}
```
Пример ответа:
```sh
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### Пример GET-запроса: получить список всех пользователей.

GET ...api/v1/users/

Пример ответа:
```sh
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```

### Пример POST-запроса: добавить нового пользователя.

POST ...api/v1/users/
```sh
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Пример ответа:
```sh
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

### Пример GET-запроса: получить пользователя по username.

GET ...api/v1/users/{username}/

Пример ответа:
```sh
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

### Пример PATCH-запроса: изменить данные пользователя по username.

PATCH ...api/v1/users/{username}/
```sh
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Пример ответа:
```sh
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
