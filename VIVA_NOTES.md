# Technical explanation and viva preparation

## Explain the stack simply
- **Frontend:** HTML/Jinja renders pages; CSS creates the dashboard layout; JavaScript recalculates bill totals as quantities change.
- **Backend:** Flask receives requests, validates inputs, applies product/stock/billing rules and selects the page to return.
- **Database:** SQLite stores products, bill headers and bill line items in a persistent file.

## Likely viva questions

**1. Why did you choose Flask?**  
It is lightweight, Python-based and sufficient for the small number of pages and business rules in this prototype.

**2. Why SQLite?**  
It provides persistent relational storage without a separate database server, making setup simple for a local assessment.

**3. What does CRUD mean?**  
Create, Read, Update and Delete. Product pages implement these operations.

**4. How is a low-stock product identified?**  
The condition is `stock <= low_stock_threshold`. Each product can have its own threshold.

**5. How is the bill total calculated?**  
Each line total is `unit_price × quantity`; the final total is the sum of the line totals.

**6. How do you prevent selling more than available stock?**  
The backend fetches the current stock inside a transaction and rejects a quantity greater than the available stock. Browser-side `max` is only a convenience, not the security check.

**7. Why use a database transaction for billing?**  
Saving a bill, its items and stock deductions must succeed together. If any check fails, rollback prevents partial changes.

**8. Why store product name and SKU in `bill_items` as well as `product_id`?**  
They are historical snapshots so a past receipt remains readable if a product is renamed or deleted.

**9. What does parameterised SQL help with?**  
It separates query structure from user-provided values and helps protect against SQL injection.

**10. What is the main limitation?**  
There is no authentication, tax/payment integration or production deployment. The app is designed for local demonstration.

**11. What would you improve next?**  
Add login/roles, GST and discounts, downloadable receipts, stock movement audit history, and deployment with secure environment configuration.

**12. What tools or AI assistance did you use?**  
Answer truthfully based on the actual work you did. Review the source code and be ready to explain every feature before the viva.

## Explain the files
- `app.py`: route handlers, validation, SQL queries and business logic.
- `templates/`: HTML page templates.
- `static/style.css`: visual design and responsive breakpoints.
- `tests/test_app.py`: repeatable tests for important workflows.
- `docs/`: requirements, architecture, test plan, demo and viva notes.
