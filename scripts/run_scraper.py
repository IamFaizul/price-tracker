from src.scraper.sites.startech import StartechScraper
from src.scraper.sites.ryans import RyansScraper
from src.db.models import save_scrape_results
import time

def run_all():
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
    
    print("All done.")

if __name__ == "__main__":
    run_all()