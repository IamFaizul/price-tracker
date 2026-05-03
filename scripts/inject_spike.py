from src.db.connection import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute(
    "INSERT INTO price_history (product_id, price, scraped_at) VALUES (?, ?, ?)",
    (1, 50000, "2026-05-02 20:00:00")
)
conn.commit()
print("Spike injected.")
conn.close()