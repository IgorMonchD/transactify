
from typing import Dict
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
import httpx

AUTH_SERVICE_URL = "http://auth_service:8000"

# Это объект, который будет извлекать токен из заголовка Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{AUTH_SERVICE_URL}/login")  # URL эндпоинта для логина


# Функция для верификации токена через микросервис аутентификации
def verify_token(token: str) -> Dict:
    try:
        response = httpx.post(f"{AUTH_SERVICE_URL}/verify-token", json={"token": token})
        response.raise_for_status()
        return response.json()  # Ожидается, что это будет JSON с данными о пользователе
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Invalid or expired token")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Authentication service is unavailable")


