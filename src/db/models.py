from src.db.connection import get_connection

def get_or_create_product(name: str, site: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT OR IGNORE INTO products (name, site) VALUES (?, ?)",
        (name, site)
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
        product_id = get_or_create_product(item["name"], item["site"])
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