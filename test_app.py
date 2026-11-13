import os
import tempfile
import unittest
from pathlib import Path

from app import app, init_db


class BusBuddyAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / 'test.db'
        app.config.update(TESTING=True, DATABASE=str(self.db_path), SECRET_KEY='test-secret')
        with app.app_context():
            init_db()
        self.client = app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_dashboard_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
        self.assertIn(b'Low-stock products', response.data)

    def test_products_page_and_search(self):
        response = self.client.get('/products?q=Daily')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bus Pass - Daily', response.data)
        self.assertNotIn(b'Bus Pass - Monthly', response.data)

    def test_add_product_and_duplicate_sku_validation(self):
        payload = {'sku': 'TEST-01', 'name': 'Test Item', 'category': 'Test', 'price': '10.5', 'stock': '8', 'low_stock_threshold': '2'}
        response = self.client.post('/products/add', data=payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Item', response.data)
        payload['name'] = 'Duplicate SKU Item'
        response = self.client.post('/products/add', data=payload, follow_redirects=True)
        self.assertIn(b'That SKU already exists', response.data)

    def test_stock_cannot_become_negative(self):
        response = self.client.post('/stock', data={'product_id': '1', 'change': '-999'}, follow_redirects=True)
        self.assertIn(b'Stock cannot become negative', response.data)
        with app.app_context():
            from app import get_db
            stock = get_db().execute('SELECT stock FROM products WHERE id=1').fetchone()['stock']
            self.assertEqual(stock, 45)

    def test_successful_bill_deducts_stock(self):
        response = self.client.post('/billing', data={'customer_name': 'Test Customer', 'qty_1': '2'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Customer', response.data)
        with app.app_context():
            from app import get_db
            db = get_db()
            stock = db.execute('SELECT stock FROM products WHERE id=1').fetchone()['stock']
            bill = db.execute('SELECT total FROM bills ORDER BY id DESC LIMIT 1').fetchone()
            self.assertEqual(stock, 43)
            self.assertAlmostEqual(bill['total'], 80.00)

    def test_insufficient_stock_does_not_create_bill(self):
        response = self.client.post('/billing', data={'customer_name': 'Test Customer', 'qty_4': '100'}, follow_redirects=True)
        self.assertIn(b'Not enough stock', response.data)
        with app.app_context():
            from app import get_db
            db = get_db()
            bill_count = db.execute('SELECT COUNT(*) FROM bills').fetchone()[0]
            stock = db.execute('SELECT stock FROM products WHERE id=4').fetchone()['stock']
            self.assertEqual(bill_count, 0)
            self.assertEqual(stock, 4)

    def test_bill_detail_404_for_unknown_id(self):
        self.assertEqual(self.client.get('/bills/99999').status_code, 404)


if __name__ == '__main__':
    unittest.main()
