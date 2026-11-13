# Architecture and data flow

## Architecture diagram

```text
┌──────────────────────────────────────────────────────┐
│                    Browser UI                         │
│ Dashboard | Products | Stock | Billing | Sales         │
│ HTML/Jinja templates + CSS + vanilla JavaScript        │
└──────────────────────────┬───────────────────────────┘
                           │ HTTP request / form submit
                           ▼
┌──────────────────────────────────────────────────────┐
│                   Flask application                   │
│ Routes / input validation / business rules / messages  │
│ app.py: dashboard, CRUD, stock adjustment, billing     │
└──────────────────────────┬───────────────────────────┘
                           │ parameterised SQL
                           ▼
┌──────────────────────────────────────────────────────┐
│                    SQLite database                    │
│ products ───────┐                                     │
│ bills ──────────┼── bill_items                         │
│                 └── FK relationships                   │
└──────────────────────────────────────────────────────┘
```

## Billing workflow

```text
User enters customer + quantities
          │
          ▼
Validate positive quantities and selected product IDs
          │
          ▼
BEGIN IMMEDIATE transaction
          │
          ├── Check each product exists and has enough stock
          ├── Calculate line totals and bill total
          ├── Insert bill header
          ├── Insert bill item snapshots
          └── Deduct stock from products
          │
          ▼
COMMIT ──► show bill receipt

Any validation/database error ──► ROLLBACK; no partial bill/stock change
```

## Database schema

- `products`: `id` primary key, unique `sku`, `name`, `category`, `price`, `stock`, `low_stock_threshold`, `created_at`.
- `bills`: `id` primary key, `customer_name`, `total`, `created_at`.
- `bill_items`: `id` primary key, `bill_id` foreign key to bills, nullable `product_id` foreign key to products, and snapshots of `product_name`, `sku`, `quantity`, `unit_price`, `line_total`.

Bill item name/SKU/price snapshots preserve the historical receipt if a product is later renamed or deleted. The database uses foreign-key constraints and numeric checks. SQLite transaction handling prevents a partial bill if stock validation fails.

## Key implementation decisions
- **Flask:** lightweight routing and server-rendered pages suitable for a small assessment project.
- **SQLite:** persistent local database with no separate server installation.
- **Server-side validation:** browser constraints improve UX but are not trusted as the only validation.
- **Transactional billing:** bill, lines and stock deduction commit together or roll back together.
- **Vanilla JavaScript:** live bill total without adding a frontend framework.
- **Demo branding:** BusBuddy and seeded bus-related products make the interface coherent while retaining the selected P08 inventory/billing problem.
