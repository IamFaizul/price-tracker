from src.db.connection import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT id, name, image_url FROM products WHERE site = 'startech' LIMIT 3")
for row in cursor.fetchall():
    print(dict(row))
conn.close()