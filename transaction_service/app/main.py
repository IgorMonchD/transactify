from fastapi import FastAPI, Depends
from . import models, crud, schemas, transactions
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/transfer", response_model=schemas.TransactionResponse)
def transfer(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    user = get_current_user(db)
    return transactions.create_transaction(db, user.id, transaction.receiver_id, transaction.amount)
