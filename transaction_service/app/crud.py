from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models


def get_balance(db: Session, user_id: int) -> float:
    """
    Функция для получения баланса пользователя
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.balance


def create_transaction(db: Session, from_user_id: int, to_user_id: int, amount: float) -> models.Transaction:
    """
    Функция для создания транзакции
    """
    # Проверяем, есть ли пользователи
    from_user = db.query(models.User).filter(models.User.id == from_user_id).first()
    to_user = db.query(models.User).filter(models.User.id == to_user_id).first()

    if not from_user or not to_user:
        raise HTTPException(status_code=404, detail="User(s) not found")

    if from_user.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Выполняем перевод средств
    from_user.balance -= amount
    to_user.balance += amount

    # Создаем запись о транзакции
    transaction = models.Transaction(
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        amount=amount,
        status="completed"
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    # Логируем успешную транзакцию
    logger.info(f"Transaction completed: {from_user_id} -> {to_user_id} amount: {amount}")

    return transaction


def get_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> list:
    """
    Функция для получения списка транзакций пользователя
    """
    transactions = db.query(models.Transaction).filter(
        (models.Transaction.from_user_id == user_id) | (models.Transaction.to_user_id == user_id)
    ).offset(skip).limit(limit).all()
    return transactions
