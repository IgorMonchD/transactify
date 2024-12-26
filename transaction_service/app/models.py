from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    sender_id = Column(Integer)  # ID отправителя
    receiver_id = Column(Integer)  # ID получателя
    status = Column(String, default="pending")
    timestamp = Column(String)

    # Связь с таблицей User
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sender_transactions")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="receiver_transactions")
