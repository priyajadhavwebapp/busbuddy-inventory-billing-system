# BusBuddy — Inventory & Billing System

A small full-stack web application built for the **P08 – Inventory and Billing System** assignment. “BusBuddy” is the demo brand and sample catalogue theme; the application demonstrates product management, stock tracking, billing, and sales reporting.

> **Important:** This is an educational prototype, not a production point-of-sale system. It uses sample data and a local SQLite database. Review, run, understand, and personalise the project before presenting it as your work. The assignment asks candidates to disclose AI tools and third-party code used.

## Features

- **Dashboard:** product count, total units, low-stock count, today's sales, all-time sales, last-seven-day sales chart, recent bills and stock alerts.
- **Product CRUD:** add, view, edit and delete products; unique SKU validation; category, price, stock and low-stock threshold.
- **Stock updates:** increase/decrease stock while preventing negative stock.
- **Billing:** choose quantities, live line totals and bill total, customer name, server-side validation, bill receipt, print-friendly bill.
- **Automatic inventory deduction:** creating a bill reduces stock in a single database transaction; insufficient stock cancels the whole bill.
- **Search:** search products by name/SKU/category and sales by customer/bill number; filter products by category.
- **Persistence:** SQLite database saved under `instance/busbuddy.db` after the app starts.
- **Usability:** responsive layout, success/error messages, empty states, and basic 404 handling.

## Technology stack

- Python 3.10+
- Flask (web framework and routes)
- SQLite (persistent relational data store)
- HTML5, CSS3, vanilla JavaScript (responsive UI and live bill calculations)
- Python `unittest` (automated route and workflow checks)

## Requirements

- Python 3.10 or newer
- pip
- A modern browser
- Internet is not required for core app behaviour. The optional Google Fonts import falls back to system fonts if unavailable.

## Run on Windows

1. Extract the ZIP file into a folder.
2. Open Command Prompt/PowerShell in that folder.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```
4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```
5. Start the app:

   ```powershell
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser.

Alternative: double-click `run_windows.bat`. If Windows blocks the script, use the commands above.

## Run on macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`.

## Sample data

On first launch, the app inserts six demo products (bus passes, travel card, route map and water bottle). If you want a clean database, stop the server, delete `instance/busbuddy.db`, and restart the app. This resets demo bills and product changes too.

## Main workflow to demonstrate

1. Open the dashboard and explain each KPI and the low-stock warning.
2. Go to **Products → Add product** and add a product with a unique SKU.
3. Search for that product and edit its price or stock threshold.
4. Open **Stock updates**, select a product and add units; show that a negative change cannot reduce stock below zero.
5. Open **Create bill**, enter a customer name, add quantities and generate the bill.
6. Show the printable receipt and explain that stock was deducted.
7. Open **Sales records**, search for the customer/bill number, and open the saved bill.
8. Return to the dashboard to show the updated sales and inventory indicators.

## Project structure

```text
BusBuddy_Inventory_Billing/
├── app.py                    # Flask routes, validation and business logic
├── requirements.txt
├── run_windows.bat
├── templates/                 # Jinja HTML pages
├── static/style.css           # Responsive UI styling
├── docs/
│   ├── PRD.md                 # Problem, scope, users and requirements
│   ├── ARCHITECTURE.md        # Architecture/data model/flow
│   ├── TEST_PLAN.md           # Test cases and results template
│   ├── DEMO_SCRIPT.md         # 2–3 minute walkthrough
│   └── VIVA_NOTES.md          # Technical explanation and viva practice
└── tests/test_app.py          # Automated tests
```

## Run automated tests

```bash
python -m unittest discover -s tests -v
```

Tests use a temporary SQLite database and do not change your demo database.

## Security and limitations

- No login/roles, tax/GST calculation, refunds, payment gateway, PDF export or cloud deployment.
- The Flask secret key is a development placeholder. Replace it and disable debug mode before any deployment.
- This prototype is intended for local demonstration; it has not been security-audited or load-tested.
- Bills use sample prices and do not represent actual transport services or actual sales.
- Dashboard chart uses locally generated demo bill history; it starts empty until you create bills.

## Future improvements

1. Add authentication and role-based permissions for admin/cashier.
2. Add GST/tax, discounts, refunds and downloadable PDF receipts.
3. Add stock movement audit history and supplier/purchase records.
4. Deploy to a hosted service with managed database and environment-based secrets.
5. Add CSV export, pagination, and more advanced date-range sales reports.

## AI/tools disclosure template

Edit this to truthfully match your actual workflow before submission:

> AI assistance was used for [planning / initial code scaffolding / debugging / documentation — keep only what applies]. The application uses Python, Flask, SQLite, HTML, CSS and JavaScript. I reviewed and tested the project and can explain the routes, data model, validation, transaction logic and limitations. Third-party dependencies are listed in `requirements.txt`.

Do not claim you wrote or independently tested anything you have not reviewed yourself.
