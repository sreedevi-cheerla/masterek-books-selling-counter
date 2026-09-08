from typing import Optional
from pydantic import BaseModel, Field, model_validator

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

class BookUpdate(BaseModel):
    original_price: Optional[float] = Field(default=None, gt=0)
    discount_percentage: Optional[float] = Field(default=None, ge=0, le=100)

    @model_validator(mode="after")
    def validate_update_values(self):
        if self.original_price is None and self.discount_percentage is None:
            raise ValueError("Provide an original price or discount percentage.")
        return self

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
