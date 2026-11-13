from flask import Flask, render_template, request, redirect, url_for, flash, g, abort
import sqlite3
from pathlib import Path
from datetime import datetime, date

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'instance' / 'busbuddy.db'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-before-deployment'
app.config['DATABASE'] = str(DB_PATH)


def get_db():
    if 'db' not in g:
        Path(app.config['DATABASE']).parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        category TEXT NOT NULL DEFAULT 'General',
        price REAL NOT NULL CHECK(price >= 0),
        stock INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0),
        low_stock_threshold INTEGER NOT NULL DEFAULT 5 CHECK(low_stock_threshold >= 0),
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        total REAL NOT NULL CHECK(total >= 0),
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS bill_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_id INTEGER NOT NULL REFERENCES bills(id) ON DELETE CASCADE,
        product_id INTEGER REFERENCES products(id) ON DELETE SET NULL,
        product_name TEXT NOT NULL,
        sku TEXT NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        unit_price REAL NOT NULL CHECK(unit_price >= 0),
        line_total REAL NOT NULL CHECK(line_total >= 0)
    );
    ''')
    count = db.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    if count == 0:
        samples = [
            ('BB-001', 'Bus Pass - Daily', 'Passes', 40.00, 45, 10),
            ('BB-002', 'Bus Pass - Weekly', 'Passes', 220.00, 18, 5),
            ('BB-003', 'Bus Pass - Monthly', 'Passes', 750.00, 12, 5),
            ('BB-004', 'Student Travel Card', 'Cards', 100.00, 4, 8),
            ('BB-005', 'Route Map', 'Accessories', 25.00, 30, 8),
            ('BB-006', 'Reusable Water Bottle', 'Accessories', 180.00, 3, 5),
        ]
        db.executemany('INSERT INTO products (sku,name,category,price,stock,low_stock_threshold) VALUES (?,?,?,?,?,?)', samples)
    db.commit()


@app.before_request
def ensure_db():
    init_db()


def money(value):
    return f'₹{float(value or 0):,.2f}'

app.jinja_env.filters['money'] = money


def product_form_values(form):
    sku = form.get('sku', '').strip().upper()
    name = form.get('name', '').strip()
    category = form.get('category', 'General').strip() or 'General'
    try:
        price = float(form.get('price', ''))
        stock = int(form.get('stock', ''))
        threshold = int(form.get('low_stock_threshold', '5'))
    except (ValueError, TypeError):
        raise ValueError('Price, stock and low-stock threshold must be valid numbers.')
    if not sku or not name:
        raise ValueError('SKU and product name are required.')
    if price < 0 or stock < 0 or threshold < 0:
        raise ValueError('Price, stock and threshold cannot be negative.')
    return sku, name, category, price, stock, threshold


@app.route('/')
def dashboard():
    db = get_db()
    product_count = db.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    stock_units = db.execute('SELECT COALESCE(SUM(stock),0) FROM products').fetchone()[0]
    low_stock_count = db.execute('SELECT COUNT(*) FROM products WHERE stock <= low_stock_threshold').fetchone()[0]
    today_sales = db.execute("SELECT COALESCE(SUM(total),0) FROM bills WHERE date(created_at)=date('now','localtime')").fetchone()[0]
    total_sales = db.execute('SELECT COALESCE(SUM(total),0) FROM bills').fetchone()[0]
    recent_bills = db.execute('SELECT * FROM bills ORDER BY id DESC LIMIT 6').fetchall()
    low_stock = db.execute('SELECT * FROM products WHERE stock <= low_stock_threshold ORDER BY stock ASC LIMIT 6').fetchall()
    chart_rows = db.execute("SELECT date(created_at) day, SUM(total) total FROM bills WHERE created_at >= datetime('now','-6 days','localtime') GROUP BY date(created_at) ORDER BY day").fetchall()
    chart = {row['day']: row['total'] for row in chart_rows}
    labels, values = [], []
    for offset in range(6, -1, -1):
        day = date.today().fromordinal(date.today().toordinal()-offset)
        labels.append(day.strftime('%d %b'))
        values.append(round(float(chart.get(day.isoformat(), 0)), 2))
    return render_template('dashboard.html', product_count=product_count, stock_units=stock_units,
        low_stock_count=low_stock_count, today_sales=today_sales, total_sales=total_sales,
        recent_bills=recent_bills, low_stock=low_stock, chart_labels=labels, chart_values=values)


@app.route('/products')
def products():
    db = get_db()
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    sql = 'SELECT * FROM products WHERE (name LIKE ? OR sku LIKE ? OR category LIKE ?)'
    args = [f'%{q}%', f'%{q}%', f'%{q}%']
    if category:
        sql += ' AND category = ?'
        args.append(category)
    sql += ' ORDER BY name COLLATE NOCASE'
    rows = db.execute(sql, args).fetchall()
    categories = [r['category'] for r in db.execute('SELECT DISTINCT category FROM products ORDER BY category')]
    return render_template('products.html', products=rows, q=q, category=category, categories=categories)


@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        try:
            values = product_form_values(request.form)
            db = get_db()
            db.execute('INSERT INTO products (sku,name,category,price,stock,low_stock_threshold) VALUES (?,?,?,?,?,?)', values)
            db.commit()
            flash('Product added successfully.', 'success')
            return redirect(url_for('products'))
        except ValueError as exc:
            flash(str(exc), 'error')
        except sqlite3.IntegrityError:
            flash('That SKU already exists. Use a unique SKU.', 'error')
    return render_template('product_form.html', product=None, page_title='Add product')


@app.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    db = get_db()
    product = db.execute('SELECT * FROM products WHERE id=?', (product_id,)).fetchone()
    if not product:
        abort(404)
    if request.method == 'POST':
        try:
            values = product_form_values(request.form)
            db.execute('UPDATE products SET sku=?,name=?,category=?,price=?,stock=?,low_stock_threshold=? WHERE id=?', (*values, product_id))
            db.commit()
            flash('Product updated successfully.', 'success')
            return redirect(url_for('products'))
        except ValueError as exc:
            flash(str(exc), 'error')
        except sqlite3.IntegrityError:
            flash('That SKU already exists. Use a unique SKU.', 'error')
    return render_template('product_form.html', product=product, page_title='Edit product')


@app.route('/products/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    db = get_db()
    product = db.execute('SELECT * FROM products WHERE id=?', (product_id,)).fetchone()
    if not product:
        abort(404)
    db.execute('DELETE FROM products WHERE id=?', (product_id,))
    db.commit()
    flash('Product deleted. Historical bill items are retained.', 'success')
    return redirect(url_for('products'))


@app.route('/stock', methods=['GET', 'POST'])
def stock_update():
    db = get_db()
    if request.method == 'POST':
        try:
            product_id = int(request.form.get('product_id', ''))
            change = int(request.form.get('change', ''))
            product = db.execute('SELECT * FROM products WHERE id=?', (product_id,)).fetchone()
            if not product:
                raise ValueError('Select a valid product.')
            new_stock = product['stock'] + change
            if new_stock < 0:
                raise ValueError('Stock cannot become negative.')
            db.execute('UPDATE products SET stock=? WHERE id=?', (new_stock, product_id))
            db.commit()
            flash(f"Stock updated for {product['name']}: {product['stock']} → {new_stock}.", 'success')
            return redirect(url_for('stock_update'))
        except (ValueError, TypeError):
            flash('Enter a valid stock change. Stock cannot become negative.', 'error')
    product_rows = db.execute('SELECT * FROM products ORDER BY name').fetchall()
    return render_template('stock.html', products=product_rows)


@app.route('/billing', methods=['GET', 'POST'])
def billing():
    db = get_db()
    product_rows = db.execute('SELECT * FROM products WHERE stock > 0 ORDER BY name').fetchall()
    if request.method == 'POST':
        customer = request.form.get('customer_name', '').strip() or 'Walk-in Customer'
        quantities = {}
        for key, value in request.form.items():
            if key.startswith('qty_'):
                try:
                    pid, qty = int(key[4:]), int(value or 0)
                except ValueError:
                    flash('Invalid product quantity.', 'error')
                    return redirect(url_for('billing'))
                if qty < 0:
                    flash('Quantity cannot be negative.', 'error')
                    return redirect(url_for('billing'))
                if qty:
                    quantities[pid] = qty
        if not quantities:
            flash('Add at least one product quantity to create a bill.', 'error')
            return redirect(url_for('billing'))
        try:
            db.execute('BEGIN IMMEDIATE')
            selected = []
            total = 0.0
            for pid, qty in quantities.items():
                product = db.execute('SELECT * FROM products WHERE id=?', (pid,)).fetchone()
                if not product:
                    raise ValueError('A selected product no longer exists.')
                if qty > product['stock']:
                    raise ValueError(f"Not enough stock for {product['name']}. Available: {product['stock']}.")
                line_total = round(product['price'] * qty, 2)
                selected.append((product, qty, line_total))
                total += line_total
            cursor = db.execute('INSERT INTO bills (customer_name,total) VALUES (?,?)', (customer, round(total, 2)))
            bill_id = cursor.lastrowid
            for product, qty, line_total in selected:
                db.execute('INSERT INTO bill_items (bill_id,product_id,product_name,sku,quantity,unit_price,line_total) VALUES (?,?,?,?,?,?,?)',
                    (bill_id, product['id'], product['name'], product['sku'], qty, product['price'], line_total))
                db.execute('UPDATE products SET stock=stock-? WHERE id=?', (qty, product['id']))
            db.commit()
            flash('Bill generated and stock updated.', 'success')
            return redirect(url_for('bill_detail', bill_id=bill_id))
        except ValueError as exc:
            db.rollback()
            flash(str(exc), 'error')
            return redirect(url_for('billing'))
        except sqlite3.Error:
            db.rollback()
            flash('Could not create the bill. Please try again.', 'error')
            return redirect(url_for('billing'))
    return render_template('billing.html', products=product_rows)


@app.route('/bills/<int:bill_id>')
def bill_detail(bill_id):
    db = get_db()
    bill = db.execute('SELECT * FROM bills WHERE id=?', (bill_id,)).fetchone()
    if not bill:
        abort(404)
    items = db.execute('SELECT * FROM bill_items WHERE bill_id=? ORDER BY id', (bill_id,)).fetchall()
    return render_template('bill_detail.html', bill=bill, items=items)


@app.route('/sales')
def sales():
    db = get_db()
    q = request.args.get('q', '').strip()
    bills = db.execute('''SELECT b.*, COUNT(i.id) item_count FROM bills b
        LEFT JOIN bill_items i ON i.bill_id=b.id
        WHERE b.customer_name LIKE ? OR CAST(b.id AS TEXT) LIKE ?
        GROUP BY b.id ORDER BY b.id DESC''', (f'%{q}%', f'%{q}%')).fetchall()
    total = db.execute('SELECT COALESCE(SUM(total),0) FROM bills').fetchone()[0]
    return render_template('sales.html', bills=bills, q=q, total=total)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
