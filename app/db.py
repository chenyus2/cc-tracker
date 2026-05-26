import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.environ.get("DB_PATH", Path(__file__).parent / "cashback.db"))


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            issuer TEXT,
            last_four TEXT,
            annual_fee REAL DEFAULT 0,
            open_date TEXT,
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );

        INSERT OR IGNORE INTO categories (name) VALUES
            ('Groceries'), ('Dining'), ('Gas'), ('Travel'),
            ('Online Shopping'), ('Streaming'), ('Utilities'),
            ('Drug Stores'), ('Home Improvement'), ('Entertainment'),
            ('Transit'), ('Wholesale Clubs'), ('Other');

        CREATE TABLE IF NOT EXISTS rewards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            reward_type TEXT NOT NULL DEFAULT 'cashback',
            reward_percent REAL NOT NULL,
            start_date TEXT,
            end_date TEXT,
            is_rotating INTEGER DEFAULT 0,
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (card_id) REFERENCES cards(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );

        CREATE TABLE IF NOT EXISTS coupons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            merchant TEXT,
            discount_type TEXT DEFAULT 'percent',
            discount_value REAL,
            min_spend REAL,
            start_date TEXT,
            end_date TEXT,
            used INTEGER DEFAULT 0,
            used_date TEXT,
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (card_id) REFERENCES cards(id)
        );

        CREATE INDEX IF NOT EXISTS idx_rewards_card ON rewards(card_id);
        CREATE INDEX IF NOT EXISTS idx_coupons_card ON coupons(card_id);
        CREATE INDEX IF NOT EXISTS idx_coupons_end_date ON coupons(end_date);
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized.")
