from src.db.connection import get_connection

conn = get_connection()
cursor = conn.cursor()

for site in ['startech', 'applegadgets', 'dazzle']:
    cursor.execute(
        "SELECT id, name, image_url FROM products WHERE site = ? AND image_url IS NOT NULL LIMIT 2",
        (site,)
    )
    rows = cursor.fetchall()
    print(f"\n--- {site} ---")
    for row in rows:
        print(dict(row))

conn.close()