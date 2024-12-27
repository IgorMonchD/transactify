from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models
from .logger import log_action


def get_balance(db: Session, user_id: int) -> float:
    """
    Функция для получения баланса пользователя
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.balance


def create_transaction(db: Session, sender_id: int, receiver_id: int, amount: float) -> models.Transaction:
    """
    Функция для создания транзакции
    """
    # Проверяем, есть ли пользователи
    from_user = db.query(models.User).filter(models.User.id == sender_id).first()
    to_user = db.query(models.User).filter(models.User.id == receiver_id).first()

    if not from_user or not to_user:
        raise HTTPException(status_code=404, detail="User(s) not found")

    if from_user.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Выполняем перевод средств
    from_user.balance -= amount
    to_user.balance += amount

    # Создаем запись о транзакции
    transaction = models.Transaction(
        sender_id=sender_id,
        receiver_id=receiver_id,
        amount=amount,
        status="completed"
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    # Логируем успешную транзакцию
    log_action(from_user, f"Transaction completed: {sender_id} -> {receiver_id} amount: {amount}")

    return transaction


def get_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> list:
    """
    Функция для получения списка транзакций пользователя
    """
    transactions = db.query(models.Transaction).filter(
        (models.Transaction.sender_id == user_id) | (models.Transaction.sender_id == user_id)
    ).offset(skip).limit(limit).all()
    return transactions
