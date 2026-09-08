from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    payment_type = Column(String, nullable=False)  # "Cash" or "UPI"
    phone_number = Column(String, nullable=True)
    total_paid = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("TransactionItem", back_populates="transaction")

class TransactionItem(Base):
    __tablename__ = "transaction_items"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_item = Column(Float, nullable=False)

    transaction = relationship("Transaction", back_populates="items")
    book = relationship("Book")
