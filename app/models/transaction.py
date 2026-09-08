from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    language = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
    original_price = Column(Float, nullable=False)
    discount_percentage = Column(Float, default=0.0)
    available_copies = Column(Integer, default=0)
