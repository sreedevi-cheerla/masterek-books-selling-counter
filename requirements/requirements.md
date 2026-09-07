# Product Requirement Document (PRD)

## 1. Project Overview
* **Project Name:** Guru Pooja Book Sale Billing & Inventory System
* **Context:** A lightweight, reliable retail and inventory management application designed for the upcoming **Guru Pooja celebrations**. The system will manage the sale of **Master EK’s books**, which are available in multiple languages and categories.
* **Objective:** Enable smooth counter billing, capture specific customer details based on payment methods, track stock levels in real time, and generate Excel reports for post-sales analysis.

---

## 2. Core Features & Functional Requirements

### 2.1 Inventory Initialization
* **Excel Data Import:** System must allow an administrator to upload an initial inventory list via an Excel sheet.
* **Book Attributes:** The import tool must parse and save the following fields for each book:
  * Book Name
  * Language (e.g., Telugu, English)
  * Category (e.g., Ayurveda, Homeopathy, Spiritual)
  * Original Price
  * Discount Percentage (%)
  * Available Copies (Initial Stock Quantity)

### 2.2 Point of Sale (POS) & Counter Billing
* **Cart Management:** The operator select books and specifies the quantity for each item during checkout.
* **Price Calculation:** The system must automatically calculate:
  * **Total Price:** Cumulative original price before discounts.
  * **After-Discount Price:** The final payable amount after applying individual item discount percentages.
* **Payment Processing:** 
  * Allowed payment types are strictly **Cash** and **UPI**.
  * **Conditional Fields:** If **UPI** is selected, capturing the customer's **Phone Number** is mandatory. If **Cash** is selected, the phone number is optional.
* **Transaction Logging:** Every completed sale must log:
  * Customer Name
  * List of books purchased (including specific quantities of each)
  * Total amount paid
  * Mode of payment (Cash or UPI)
  * Customer Phone Number (if applicable)
* **Stock Update:** The system must immediately decrement the `Available Copies` of a book once a sale transaction is finalized.

### 2.3 Data Export & Reporting
The system must generate three distinct Excel report exports at regular intervals or after sales completion:
1. **Sales Summary Report:** Displays the total number of books sold globally and the cumulative financial revenue generated.
2. **Customer Transaction Log:** Outlines each customer's name, the specific books they bought, the final amount they paid, and their mode of payment.
3. **Current Stock Report:** A real-time inventory list displaying each book name alongside its remaining available copies.

---

## 3. Technology Stack Recommendation

### Option A: Java Spring Boot + SQLite (Your Initial Choice)
* **Backend:** **Java Spring Boot (REST API)**. Highly scalable and provides robust data parsing libraries like Apache POI for Excel handling.
* **Database:** **SQLite**. An excellent choice for a small project because it is serverless, zero-configuration, and stores data in a single local file.
* **Frontend:** A lightweight frontend framework like **Thymeleaf** (embedded in Spring Boot) or a simple **React/Vue** single-page application to make the counter UI fast and responsive.

### Option B: Python (Flask/FastAPI) + SQLite (Alternative Lightweight Recommendation)
* **Backend:** **Python (FastAPI or Flask)**. 
* **Pros:** Considerably faster to set up and develop for a short-term festival event. Python natively handles Excel files exceptionally fast using powerful data libraries like `pandas` and `openpyxl`, reducing the code needed for your reporting engine.

---

## 4. Non-Functional Requirements
* **Usability:** The counter interface must be optimized for rapid data entry (keyboard navigation or quick-search bars) to avoid queues at the venue.
* **Reliability:** Since it uses a local SQLite database, the system must perform automatic local file backups to an external drive or cloud storage at regular intervals to prevent data loss.
* **Offline Capability:** The system should operate perfectly without an active internet connection, except potentially when validating external UPI payment gateways (if integrated manually).
