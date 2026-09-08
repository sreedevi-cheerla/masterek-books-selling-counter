from pydantic import BaseModel, model_validator
from typing import List, Optional

class CartItem(BaseModel):
    book_id: int
    quantity: int

class CheckoutRequest(BaseModel):
    customer_name: str
    payment_type: str  # Strictly "Cash" or "UPI"
    phone_number: Optional[str] = None
    items: List[CartItem]

    @model_validator(mode="after")
    def validate_upi_phone(self):
        payment_type = self.payment_type.upper()
        if payment_type == "UPI" and not self.phone_number:
            raise ValueError("Phone number is strictly mandatory for UPI transactions.")
        return self
