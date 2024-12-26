from datetime import datetime, timedelta
from jose import JWTError, jwt  # Используйте библиотеку jose
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session  # Импортируем Session
from passlib.context import CryptContext  # Импортируем CryptContext
from . import crud, schemas

# Создаем контекст для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "F03E2408FEB325B0732DCD4BB5ADA367"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Функция для создания токена
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функция для аутентификации пользователя
def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_username(db, username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

# Функция для получения текущего пользователя
def get_current_user(db: Session, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = crud.get_user(db, payload.get("sub"))
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user
