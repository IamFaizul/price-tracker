from abc import ABC, abstractmethod
from datetime import datetime

class BaseScraper(ABC):
    
    def __init__(self, site_name: str):
        self.site_name = site_name
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    @abstractmethod
    def scrape(self) -> list[dict]:
        pass
    
    def format_result(self, name: str, price: float) -> dict:
        return {
            "site": self.site_name,
            "name": name,
            "price": price,
            "currency": "BDT",
            "scraped_at": datetime.now().isoformat()
        }