from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    receiver_id: int
    amount: float

class TransactionResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    amount: float
    status: str
    timestamp: datetime

    class Config:
        orm_mode = True

