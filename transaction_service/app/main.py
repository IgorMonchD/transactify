from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal
from . import auth  # Импортируем модуль с верификацией токена

app = FastAPI()

# Функция для получения базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Эндпоинт для перевода средств
@app.post("/transfer")
def transfer(
        transaction: schemas.TransactionCreate,
        db: Session = Depends(get_db),
        token: str = Depends(auth.oauth2_scheme)  # Токен передается через Authorization
):
    # Проверка токена через микросервис аутентификации
    user_data = auth.verify_token(token)  # Получаем информацию о пользователе через микросервис
    user_id = user_data["user_id"]

    # Проверка баланса и создание транзакции
    sender_balance = crud.get_balance(db, user_id)
    if sender_balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    return crud.create_transaction(db, user_id, transaction.receiver_id, transaction.amount)

# Эндпоинт для получения истории транзакций
@app.get("/transactions")
def get_transactions(
        skip: int = 0, limit: int = 10,
        db: Session = Depends(get_db),
        token: str = Depends(auth.oauth2_scheme)  # Токен передается через Authorization
):
    # Проверка токена через микросервис аутентификации
    user_data = auth.verify_token(token)  # Получаем информацию о пользователе через микросервис
    user_id = user_data["user_id"]

    transactions = crud.get_transactions(db, user_id, skip, limit)
    return {"transactions": transactions, "total_count": len(transactions)}
