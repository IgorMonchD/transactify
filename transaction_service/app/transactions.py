from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

def create_transaction(db: Session, sender_id: int, receiver_id: int, amount: float):
    sender = db.query(models.User).filter(models.User.id == sender_id).first()
    receiver = db.query(models.User).filter(models.User.id == receiver_id).first()
    if not sender or not receiver:
        raise HTTPException(status_code=400, detail="User not found")
    if sender.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    transaction = models.Transaction(sender_id=sender_id, receiver_id=receiver_id, amount=amount, status="completed")
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
