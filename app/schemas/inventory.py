from pydantic import BaseModel

class BookBase(BaseModel):
    name: str
    language: str
    category: str
    original_price: float
    discount_percentage: float
    available_copies: int

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
