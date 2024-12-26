import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models

# Инициализация логгера
logger = logging.getLogger(__name__)


def transfer_funds(db: Session, from_user_id: int, to_user_id: int, amount: float, description: str):
    try:
        # Проверка наличия пользователей
        from_user = db.query(models.User).filter(models.User.id == from_user_id).first()
        to_user = db.query(models.User).filter(models.User.id == to_user_id).first()

        if not from_user or not to_user:
            logger.error(f"User(s) not found: {from_user_id}, {to_user_id}")
            raise ValueError("One or both users not found.")

        if from_user.balance < amount:
            logger.error(f"Insufficient funds for user {from_user_id}: {from_user.balance} < {amount}")
            raise ValueError("Insufficient funds.")

        # Выполнение перевода
        from_user.balance -= amount
        to_user.balance += amount

        # Создание транзакции
        transaction = models.Transaction(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            amount=amount,
            description=description,
            status="completed"
        )
        db.add(transaction)
        db.commit()

        # Логирование успешной транзакции
        logger.info(f"Transaction completed: {from_user_id} -> {to_user_id} amount: {amount}")

        return transaction
    except Exception as e:
        logger.error(f"Error during transaction: {str(e)}")
        raise HTTPException(status_code=500, detail="Transaction failed")
