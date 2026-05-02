from src.scraper.sites.startech import StartechScraper
from src.scraper.sites.ryans import RyansScraper
from src.db.models import save_scrape_results, get_or_create_product, get_price_history, insert_anomaly
from src.model.inference import load_model, get_reconstruction_error
import time

THRESHOLD = 0.213

def check_anomalies(model, min_val, max_val):
    from src.db.connection import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT id FROM products")
    product_ids = [row["id"] for row in cursor.fetchall()]
    conn.close()

    anomaly_count = 0
    for pid in product_ids:
        history = get_price_history(pid)
        prices = [h["price"] for h in history]
        if len(prices) < 7:
            continue
        sequence = prices[-7:]
        error = get_reconstruction_error(model, sequence, min_val, max_val)
        if error > THRESHOLD:
            if error > THRESHOLD * 2:
                severity = "high"
            elif error > THRESHOLD * 1.5:
                severity = "medium"
            else:
                severity = "low"
            insert_anomaly(pid, error, severity)
            anomaly_count += 1
            print(f"[anomaly] product_id={pid} error={error:.4f} severity={severity}")

    print(f"Anomaly check done. {anomaly_count} anomalies detected.")

def run_all():
    print("Loading model...")
    model, min_val, max_val = load_model()

    scrapers = [
        StartechScraper(),
        RyansScraper(),
    ]

    for scraper in scrapers:
        print(f"Scraping {scraper.site_name}...")
        try:
            results = scraper.scrape()
            save_scrape_results(results)
        except Exception as e:
            print(f"[{scraper.site_name}] failed: {e}")
        time.sleep(2)

    check_anomalies(model, min_val, max_val)
    print("All done.")

if __name__ == "__main__":
    run_all()