# 2–3 minute demo script

**0:00–0:20 — Introduce the problem**  
“BusBuddy Inventory & Billing is my P08 prototype. It helps a small counter maintain a product catalogue, monitor stock, prepare bills and review sales from one dashboard. The product data and prices are sample data.”

**0:20–0:45 — Dashboard**  
“Here are the number of products, total units in stock, products at or below their low-stock threshold, and today's recorded sales. The low-stock panel helps identify items that need replenishment. The chart summarises sales from the last seven days.”

**0:45–1:10 — Product and stock management**  
“From Products, I can add, search, edit and delete items. SKU is unique, and price/stock cannot be negative. Stock updates let me record received units or corrections, while blocking negative stock.”

**1:10–1:50 — Billing and integration**  
“I enter a customer name, select quantities, and the browser calculates line totals and the bill total. When I generate the bill, the backend revalidates stock and saves the bill, its line items and stock deduction in one database transaction. If there is not enough stock, the transaction is rolled back.”

**1:50–2:15 — Receipt and sales**  
“The saved receipt is printable. Sales Records lets me search by customer or bill number and reopen a bill. The data persists in SQLite after restarting the application.”

**2:15–2:35 — Testing and limitations**  
“I wrote automated tests for core routes, product validation, stock changes and billing. This is a local educational prototype; authentication, GST, refunds and deployment are future improvements.”

## Suggested live change request to practise
Add a new product category filter or adjust the low-stock threshold of a product. Explain which route/template handles the change and test it in the browser.
