import io
import pandas as pd
from sqlalchemy.orm import Session
from app.models.inventory import Book
from app.models.transaction import Transaction, TransactionItem

class ExcelService:
    @staticmethod
    def import_inventory(file_contents: bytes, db: Session):
        df = pd.read_excel(io.BytesIO(file_contents))
        
        # Clear out existing inventory safely
        db.query(Book).delete()
        
        for _, row in df.iterrows():
            book = Book(
                name=str(row['Book Name']).strip(),
                language=str(row['Language']).strip(),
                category=str(row['Category']).strip(),
                original_price=float(row['Original Price']),
                discount_percentage=float(row['Discount Percentage (%)']),
                available_copies=int(row['Available Copies'])
            )
            db.add(book)
        db.commit()

    @staticmethod
    def generate_reports(db: Session) -> io.BytesIO:
        output = io.BytesIO()
        
        # 1. Sales Summary Data
        tx_items = db.query(TransactionItem).all()
        total_books_sold = sum(item.quantity for item in tx_items)
        total_revenue = sum(item.quantity * item.price_per_item for item in tx_items)
        df_summary = pd.DataFrame([{
            "Total Books Sold": total_books_sold,
            "Total Revenue Generated": total_revenue
        }])

        # 2. Customer Transaction Log Data
        transactions = db.query(Transaction).all()
        tx_log_data = []
        for tx in transactions:
            books_list = ", ".join([f"{item.book.name} (x{item.quantity})" for item in tx.items])
            tx_log_data.append({
                "Transaction ID": tx.id,
                "Customer Name": tx.customer_name,
                "Phone Number": tx.phone_number or "N/A",
                "Payment Mode": tx.payment_type,
                "Books Purchased": books_list,
                "Total Amount Paid": tx.total_paid,
                "Timestamp": tx.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        df_log = pd.DataFrame(tx_log_data) if tx_log_data else pd.DataFrame(columns=["Transaction ID", "Customer Name", "Phone Number", "Payment Mode", "Books Purchased", "Total Amount Paid", "Timestamp"])

        # 3. Current Stock Data
        books = db.query(Book).all()
        stock_data = [{
            "Book Name": b.name,
            "Language": b.language,
            "Category": b.category,
            "Remaining Available Copies": b.available_copies
        } for b in books]
        df_stock = pd.DataFrame(stock_data) if stock_data else pd.DataFrame(columns=["Book Name", "Language", "Category", "Remaining Available Copies"])

        # Write to multi-sheet workbook
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_summary.to_excel(writer, sheet_name="Sales Summary", index=False)
            df_log.to_excel(writer, sheet_name="Customer Transaction Log", index=False)
            df_stock.to_excel(writer, sheet_name="Current Stock Report", index=False)
            
        output.seek(0)
        return output
