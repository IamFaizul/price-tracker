import requests
from bs4 import BeautifulSoup
from src.scraper.base import BaseScraper

class StartechScraper(BaseScraper):
    
    def __init__(self):
        super().__init__(site_name="startech")
        self.urls = [
            "https://www.startech.com.bd/apple-macbook",
            "https://www.startech.com.bd/apple-iphone",
            "https://www.startech.com.bd/apple-ipad",
            "https://www.startech.com.bd/apple-airpods",
            "https://www.startech.com.bd/apple-mac-mini",
            "https://www.startech.com.bd/apple-imac",
            "https://www.startech.com.bd/apple-smart-watch",
        ]
    
    def scrape(self) -> list[dict]:
        results = []
        
        for url in self.urls:
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, "html.parser")
                products = soup.find_all("div", class_="p-item")
                
                for product in products:
                    try:
                        name = product.find(class_="p-item-name").get_text(strip=True)
                        price_text = product.find(class_="p-item-price").find("span").get_text(strip=True)
                        price = float(price_text.replace(",", "").replace("৳", "").strip())
                        results.append(self.format_result(name, price))
                    except Exception:
                        continue
                        
            except Exception as e:
                print(f"[startech] scrape failed for {url}: {e}")
        
        return results