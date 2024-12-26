from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    balance = Column(Float)

    # Связь с таблицей Transaction
    sender_transactions = relationship("Transaction", back_populates="sender", foreign_keys="Transaction.sender_id")
    receiver_transactions = relationship("Transaction", back_populates="receiver", foreign_keys="Transaction.receiver_id")