# Сервис auth_service
## 1. Регистрация пользователя

### Endpoint: 
`POST /register`

Регистрирует нового пользователя в системе.

Тело запроса (JSON):

```json
{
  "username": "example_user",
  "email": "user@example.com",
  "password": "secure_password"
}
```
Успешный ответ (200):

```json
{
  "id": 1,
  "username": "example_user",
  "email": "user@example.com"
}
```
Ошибки:
400: Имя пользователя уже зарегистрировано:

```json
{
  "detail": "Username already registered"
}
```
## 2. Авторизация пользователя

### Endpoint: 
`POST /login`

Авторизует пользователя и возвращает токен доступа.

Форм-данные:

username: Имя пользователя.
password: Пароль пользователя.
Успешный ответ (200):

```json
{
  "access_token": "generated_token",
  "token_type": "bearer"
}
```
Ошибки:
401: Неверные учетные данные:

```json
{
  "detail": "Incorrect username or password"
}
```
## 3. Смена пароля

### Endpoint: 
`POST /change-password`

Позволяет пользователю изменить пароль.

Заголовки:

Authorization: Bearer <token>
Тело запроса (JSON):

```json
{
  "new_password": "new_secure_password"
}
```
Успешный ответ (200):

```json
{
  "msg": "Password changed successfully"
}
```
Ошибки:
401: Если токен недействителен или пользователь не авторизован:

```json
{
  "detail": "Not authenticated"
}
```
## 4. Проверка токена

### Endpoint: 
`POST /verify-token`

Проверяет валидность токена и возвращает информацию о пользователе.

Тело запроса (JSON):

```json
{
  "token": "generated_token"
}
```
Успешный ответ (200):

```json
{
  "message": "Token is valid",
  "user_data": {
    "user_id": 1,
    "username": "example_user"
  }
}
```
Ошибки:
404: Если пользователь не найден:

```json
{
  "detail": "User not found"
}
```

# Сервис transaction_service

## 1. Перевод средств

### Endpoint:
`POST /transfer`

Переводит средства с баланса пользователя на другой счёт. Токен передается через заголовок Authorization.

Тело запроса (JSON)
```json
{
  "receiver_id": 2,
  "amount": 100.0
}
```
Успешный ответ (200):
```json
{
  "id": 1,
  "sender_id": 1,
  "receiver_id": 2,
  "amount": 100.0,
  "status": "completed",
  "timestamp": "2024-12-27T12:34:56"
}
```
Ошибки:
404: Баланс не найден:

```json
{
  "detail": "Balance not found"
}
```
400: Недостаточно средств:

```json
{
  "detail": "Insufficient funds"
}
```
## 2. Получение истории транзакций

### Endpoint:
`GET /transactions`

Получение списка транзакций пользователя с возможностью пагинации. Токен передается через заголовок Authorization.

Параметры запроса:
skip: Количество транзакций для пропуска (по умолчанию 0).
limit: Максимальное количество транзакций для возврата (по умолчанию 10).
Успешный ответ (200):
```json
{
  "transactions": [
    {
      "id": 1,
      "sender_id": 1,
      "receiver_id": 2,
      "amount": 100.0,
      "status": "completed",
      "timestamp": "2024-12-27T12:34:56"
    },
    {
      "id": 2,
      "sender_id": 1,
      "receiver_id": 3,
      "amount": 50.0,
      "status": "completed",
      "timestamp": "2024-12-26T11:22:33"
    }
  ],
  "total_count": 2
}
```
Ошибки:
401: Если токен недействителен или пользователь не авторизован:

```json
{
  "detail": "Not authenticated"
}
```
