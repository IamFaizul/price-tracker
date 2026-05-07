from src.db.connection import get_connection

def get_or_create_product(name: str, site: str, image_url: str = None) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT OR IGNORE INTO products (name, site, image_url) VALUES (?, ?, ?)",
        (name, site, image_url)
    )
    conn.commit()
    
    if image_url:
        cursor.execute(
            "UPDATE products SET image_url = ? WHERE name = ? AND site = ?",
            (image_url, name, site)
        )
        conn.commit()
    
    cursor.execute(
        "SELECT id FROM products WHERE name = ? AND site = ?",
        (name, site)
    )
    row = cursor.fetchone()
    conn.close()
    return row["id"]

def insert_price(product_id: int, price: float) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT price FROM price_history WHERE product_id = ? ORDER BY scraped_at DESC LIMIT 1",
        (product_id,)
    )
    last = cursor.fetchone()
    if last and last["price"] == price:
        conn.close()
        return False
    
    cursor.execute(
        "INSERT INTO price_history (product_id, price) VALUES (?, ?)",
        (product_id, price)
    )
    conn.commit()
    conn.close()
    return True

def save_scrape_results(results: list[dict]):
    inserted = 0
    for item in results:
        product_id = get_or_create_product(item["name"], item["site"], item.get("image_url"))
        if insert_price(product_id, item["price"]):
            inserted += 1
    print(f"Saved {inserted} new price records. ({len(results)} total scraped)")

def get_price_history(product_id: int) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT price, scraped_at FROM price_history WHERE product_id = ? ORDER BY scraped_at ASC",
        (product_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def insert_anomaly(product_id: int, reconstruction_error: float, severity: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO anomalies (product_id, reconstruction_error, severity) VALUES (?, ?, ?)",
        (product_id, reconstruction_error, severity)
    )
    conn.commit()
    conn.close()

def get_recent_anomalies(limit: int = 10) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, p.name, p.site, a.reconstruction_error, a.severity, a.detected_at
        FROM anomalies a
        JOIN products p ON a.product_id = p.id
        ORDER BY a.detected_at DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]