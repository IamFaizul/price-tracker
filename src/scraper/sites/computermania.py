import requests
from bs4 import BeautifulSoup
from src.scraper.base import BaseScraper

class ComputerManiaScraper(BaseScraper):
    
    def __init__(self):
        super().__init__(site_name="computermania")
        self.url = "https://computermania.com.bd/product-category/apple/"
    
    def scrape(self) -> list[dict]:
        results = []
        
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            products = soup.find_all("div", class_="wd-product-wrapper")
            
            for product in products:
                try:
                    name = product.find(["h2", "h3"]).get_text(strip=True)
                    amounts = product.find_all("span", class_="amount")
                    price_text = amounts[-1].get_text(strip=True)
                    price = float(price_text.replace("৳", "").replace(",", "").strip())
                    results.append(self.format_result(name, price))
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"[computermania] scrape failed: {e}")
        
        return results