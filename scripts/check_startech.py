from src.db.connection import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT id FROM products WHERE site = 'startech'")
ids = [r['id'] for r in cursor.fetchall()]
print(ids)
conn.close()