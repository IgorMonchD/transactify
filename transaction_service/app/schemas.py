from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    amount: float
    receiver_id: int

class TransactionResponse(BaseModel):
    id: int
    amount: float
    sender_id: int
    receiver_id: int
    status: str
    timestamp: datetime

    class Config:
        orm_mode = True
