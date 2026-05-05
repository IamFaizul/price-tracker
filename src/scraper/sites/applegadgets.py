import os
from bs4 import BeautifulSoup
from src.scraper.base import BaseScraper

class AppleGadgetsScraper(BaseScraper):

    def __init__(self):
        super().__init__(site_name="applegadgets")
        self.urls = [
            "https://www.applegadgetsbd.com/category/macbook",
            "https://www.applegadgetsbd.com/category/iphone",
            "https://www.applegadgetsbd.com/category/ipad",
            "https://www.applegadgetsbd.com/category/airpods",
            "https://www.applegadgetsbd.com/category/apple-watch",
            "https://www.applegadgetsbd.com/category/imac",
        ]

    def scrape(self) -> list[dict]:
        os.environ['PLAYWRIGHT_BROWSERS_PATH'] = 'D:\\playwright-browsers'
        from playwright.sync_api import sync_playwright

        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for url in self.urls:
                try:
                    page.goto(url, timeout=30000)
                    page.wait_for_timeout(3000)
                    page.wait_for_selector('.card-shadow', timeout=10000)
                    html = page.content()
                    soup = BeautifulSoup(html, "html.parser")
                    products = soup.find_all("article", class_="card-shadow")

                    for product in products:
                        try:
                            name = product.find(class_="line-clamp-2").get_text(strip=True)
                            price_text = product.find("span", class_="font-semibold").get_text(strip=True)
                            price = float(price_text.replace("৳", "").replace(",", "").strip())
                            results.append(self.format_result(name, price))
                        except Exception:
                            continue

                except Exception as e:
                    print(f"[applegadgets] failed for {url}: {e}")

            browser.close()

        return results