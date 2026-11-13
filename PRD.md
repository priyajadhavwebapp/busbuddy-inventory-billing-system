# Product Requirements Document (PRD)

## 1. Project overview
**Product:** BusBuddy — Inventory & Billing System  
**Assignment:** P08 — Inventory and Billing System  
**Purpose:** Provide a small web app for maintaining a product catalogue, tracking stock, preparing sample bills and reviewing sales. BusBuddy is the demo brand and gives the seed catalogue a travel/pass theme.

## 2. Problem statement
Small counters may track products and sales manually, making it harder to find items, notice low stock, calculate bills consistently and understand recent sales. The prototype centralises product records, stock updates and sample billing in one searchable application.

## 3. Users
- **Counter operator:** searches products, creates a customer bill and prints the receipt.
- **Inventory operator:** adds/edits products and adjusts stock.
- **Owner/evaluator:** checks dashboard KPIs, low-stock alerts and sales records.

These are prototype user roles; authentication and permissions are not implemented.

## 4. Goals and success criteria
- Create, read, update and delete product records.
- Prevent duplicate SKUs and invalid negative prices/stock.
- Flag products whose stock is at or below their configured threshold.
- Generate bills with correct line totals and grand total.
- Deduct stock when a bill succeeds, and reject bills exceeding available stock.
- Preserve bills and bill lines in SQLite after restarting the app.
- Search the product catalogue and sales history.
- Provide a dashboard and enough documentation for an end-to-end demonstration.

## 5. Functional requirements
| ID | Requirement | Acceptance check |
|---|---|---|
| FR-01 | Product CRUD | Add, view, edit and delete products. |
| FR-02 | SKU uniqueness | A duplicate SKU is rejected with a clear message. |
| FR-03 | Stock adjustment | Stock can be increased/decreased but cannot become negative. |
| FR-04 | Low-stock warning | Product is flagged when `stock <= low_stock_threshold`. |
| FR-05 | Bill creation | User selects one or more products and quantities. |
| FR-06 | Bill arithmetic | Line total = unit price × quantity; bill total is sum of line totals. |
| FR-07 | Inventory integration | Successful bill deducts quantities from stock. Failed bill does not create a partial transaction. |
| FR-08 | Sales history | Created bills persist and can be searched/opened. |
| FR-09 | Dashboard | Show catalogue count, units, low-stock count, daily sales and recent bills. |
| FR-10 | Input/error handling | Required fields and numeric bounds are validated; user sees useful error messages. |

## 6. Non-functional requirements
- Responsive browser interface.
- Simple project layout and setup instructions.
- SQLite persistence without separate database-server setup.
- Use parameterised SQL queries and database foreign-key constraints.
- Keep billing writes in a database transaction.
- Local demonstration startup target: under a few minutes after dependencies are installed.

## 7. Scope
**In scope:** local single-user prototype, product catalogue, stock changes, low-stock alerts, sample billing, sales list/search, dashboard, tests and documentation.  
**Out of scope:** real payments, login, role management, tax/GST, refunds, cloud deployment, supplier purchasing, multi-branch stock, barcode scanning and production security.

## 8. Main user flow
Open dashboard → manage products/stock → create bill → validate quantities → calculate total → save bill and line items → deduct stock atomically → show receipt → review sales history and dashboard.

## 9. Risks and assumptions
- Seed products and prices are fictional and must not be treated as real-world pricing.
- The application assumes one local operator and a local SQLite file.
- A real production deployment would need authentication, backups, security review, audit logging and tax/payment requirements.

## 10. Future enhancements
Authentication and roles; tax/discounts/refunds; PDF and CSV exports; supplier and stock-movement audit history; date-range analytics; deployment with environment-based secrets.
