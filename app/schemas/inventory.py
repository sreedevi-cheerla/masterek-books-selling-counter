from pydantic import BaseModel, Field

class BookBase(BaseModel):
    name: str
    language: str
    category: str
    original_price: float
    discount_percentage: float
    available_copies: int

class BookCreate(BookBase):
    original_price: float = Field(gt=0)
    discount_percentage: float = Field(ge=0, le=100)
    available_copies: int = Field(ge=0)

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
