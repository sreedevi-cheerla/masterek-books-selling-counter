from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inventory import Book
from app.models.transaction import Transaction, TransactionItem
from app.schemas.transaction import CheckoutRequest
from app.services.backup_service import BackupService

router = APIRouter(prefix="/billing", tags=["POS Counter Billing"])

@router.post("/checkout")
def checkout(payload: CheckoutRequest, db: Session = Depends(get_db)):
    running_total = 0.0
    items_to_save = []

    for cart_item in payload.items:
        book = db.query(Book).filter(Book.id == cart_item.book_id).first()
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {cart_item.book_id} missing.")
        
        if book.available_copies < cart_item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Insufficient copies for '{book.name}'. Requested: {cart_item.quantity}, In Stock: {book.available_copies}"
            )

        # Price Deductions Strategy Calculations
        discount_amount = book.original_price * (book.discount_percentage / 100.0)
        final_unit_price = book.original_price - discount_amount
        running_total += final_unit_price * cart_item.quantity

        # Decrement Inventory Volumes Immediately
        book.available_copies -= cart_item.quantity
        
        items_to_save.append({
            "book_id": book.id,
            "quantity": cart_item.quantity,
            "price_per_item": final_unit_price
        })

    # Record Consolidated Retail Receipt
    transaction = Transaction(
        customer_name=payload.customer_name,
        payment_type=payload.payment_type.upper(),
        phone_number=payload.phone_number,
        total_paid=running_total
    )
    db.add(transaction)
    db.flush()  # Extract the auto-increment transaction ID

    for item in items_to_save:
        tx_item = TransactionItem(
            transaction_id=transaction.id,
            book_id=item["book_id"],
            quantity=item["quantity"],
            price_per_item=item["price_per_item"]
        )
        db.add(tx_item)

    db.commit()
    
    # Run immediate local automated safety backup routine
    BackupService.trigger_local_backup()
    
    return {"status": "success", "transaction_id": transaction.id, "total_payable": running_total}
