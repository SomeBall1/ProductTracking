"""Database operations for product tracking using built-in sqlite3."""
import sqlite3
from datetime import datetime
from config import Config


class ProductCheck:
    """Simple data class for product checks."""

    def __init__(self, id, location_name, location_url, product_name, is_available, price, checked_at):
        self.id = id
        self.location_name = location_name
        self.location_url = location_url
        self.product_name = product_name
        self.is_available = is_available
        self.price = price
        self.checked_at = checked_at

    def __repr__(self):
        return f"<ProductCheck(location='{self.location_name}', available={self.is_available}, time={self.checked_at})>"


class Database:
    """Database manager for product tracking using sqlite3."""

    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.conn = None
        self._connect()
        self._create_tables()

    def _connect(self):
        """Connect to the database."""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def _create_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location_name TEXT NOT NULL,
                location_url TEXT NOT NULL,
                product_name TEXT NOT NULL,
                is_available INTEGER NOT NULL,
                price TEXT,
                checked_at TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_check(self, location_name, location_url, product_name, is_available, price=None):
        """Add a new product check to the database."""
        cursor = self.conn.cursor()
        checked_at = datetime.utcnow().isoformat()

        cursor.execute('''
            INSERT INTO product_checks (location_name, location_url, product_name, is_available, price, checked_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (location_name, location_url, product_name, 1 if is_available else 0, price, checked_at))

        self.conn.commit()

        return ProductCheck(
            cursor.lastrowid,
            location_name,
            location_url,
            product_name,
            is_available,
            price,
            checked_at
        )

    def get_last_check(self, location_name):
        """Get the most recent check for a location."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM product_checks
            WHERE location_name = ?
            ORDER BY checked_at DESC
            LIMIT 1
        ''', (location_name,))

        row = cursor.fetchone()
        if row:
            return ProductCheck(
                row['id'],
                row['location_name'],
                row['location_url'],
                row['product_name'],
                bool(row['is_available']),
                row['price'],
                row['checked_at']
            )
        return None

    def get_availability_history(self, location_name, limit=10):
        """Get recent availability history for a location."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM product_checks
            WHERE location_name = ?
            ORDER BY checked_at DESC
            LIMIT ?
        ''', (location_name, limit))

        results = []
        for row in cursor.fetchall():
            results.append(ProductCheck(
                row['id'],
                row['location_name'],
                row['location_url'],
                row['product_name'],
                bool(row['is_available']),
                row['price'],
                row['checked_at']
            ))
        return results

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
