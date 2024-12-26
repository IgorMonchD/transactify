from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    sender_id = Column(Integer)
    receiver_id = Column(Integer)
    status = Column(String, default="pending")
    timestamp = Column(String)