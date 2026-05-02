from apscheduler.schedulers.background import BackgroundScheduler
from src.scraper.sites.startech import StartechScraper
from src.scraper.sites.ryans import RyansScraper
from src.db.models import save_scrape_results
import time

def scrape_and_save():
    scrapers = [
        StartechScraper(),
        RyansScraper(),
    ]
    
    for scraper in scrapers:
        print(f"[scheduler] Scraping {scraper.site_name}...")
        try:
            results = scraper.scrape()
            save_scrape_results(results)
        except Exception as e:
            print(f"[scheduler] {scraper.site_name} failed: {e}")
        time.sleep(2)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        scrape_and_save,
        trigger="interval",
        hours=3,
        id="price_scraper"
    )
    scheduler.start()
    print("Scheduler started. Scraping every 3 hours.")
    return scheduler

if __name__ == "__main__":
    scrape_and_save()
    scheduler = start_scheduler()
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        scheduler.shutdown()
        print("Scheduler stopped.")