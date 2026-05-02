import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../data/prices.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            site TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(name, site)
        );
        
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER REFERENCES products(id),
            price REAL NOT NULL,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS anomalies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER REFERENCES products(id),
            detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reconstruction_error REAL,
            severity TEXT,
            notified INTEGER DEFAULT 0
        );
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized.")