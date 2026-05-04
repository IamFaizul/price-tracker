import os
import requests as req
from src.scraper.sites.startech import StartechScraper
from src.scraper.sites.ryans import RyansScraper
from src.db.models import save_scrape_results, get_price_history, insert_anomaly
from src.model.inference import load_model, get_reconstruction_error
import time

THRESHOLD = 0.213
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_alert(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[telegram] credentials not found, skipping alert")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        req.post(url, json=payload, timeout=10)
        print("[telegram] alert sent")
    except Exception as e:
        print(f"[telegram] failed: {e}")

def check_anomalies(model, min_val, max_val):
    from src.db.connection import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT id, name FROM products")
    products = [(row["id"], row["name"]) for row in cursor.fetchall()]
    conn.close()

    anomaly_count = 0
    for pid, name in products:
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

            severity_emoji = "🔴 High" if severity == "high" else "🟡 Medium" if severity == "medium" else "🟢 Low"

            message = (
                f"🚨 <b>Price Alert — {name}</b>\n\n"
                f"An unusual price movement has been detected.\n\n"
                f"Severity: {severity_emoji}\n\n"
                f"👉 <a href='https://cost-insight-station.lovable.app/price-history/{pid}'>View Price History</a>"
            )
            send_telegram_alert(message)

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