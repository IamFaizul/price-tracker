import os
from bs4 import BeautifulSoup
from src.scraper.base import BaseScraper

class DazzleScraper(BaseScraper):

    def __init__(self):
        super().__init__(site_name="dazzle")
        self.urls = [
    "https://dazzle.com.bd/categories/laptop/apple-macbook",
    "https://dazzle.com.bd/categories/phones/iphone",
    "https://dazzle.com.bd/categories/tablet/ipad",
    "https://dazzle.com.bd/categories/smart-watch/apple-watch",
    "https://dazzle.com.bd/categories/gadget/airpods",
]

    def scrape(self) -> list[dict]:
        os.environ['PLAYWRIGHT_BROWSERS_PATH'] = 'D:\\playwright-browsers'
        from playwright.sync_api import sync_playwright

        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = context.new_page()

            for url in self.urls:
                try:
                    page.goto(url, timeout=30000)
                    page.wait_for_timeout(5000)
                    html = page.content()
                    soup = BeautifulSoup(html, "html.parser")
                    products = soup.find_all("a", class_="line-clamp-2")

                    for product in products:
                        try:
                            name = product.get_text(strip=True)
                            price_el = product.find_next("span", class_="font-semibold")
                            price_text = price_el.get_text(strip=True)
                            price = float(price_text.replace("৳", "").replace(",", "").strip())
                            results.append(self.format_result(name, price))
                        except Exception:
                            continue

                except Exception as e:
                    print(f"[dazzle] failed for {url}: {e}")

            browser.close()

        return results