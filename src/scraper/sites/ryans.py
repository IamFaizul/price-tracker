import os
from bs4 import BeautifulSoup
from src.scraper.base import BaseScraper

class RyansScraper(BaseScraper):

    def __init__(self):
        super().__init__(site_name="ryans")
        self.urls = [
            "https://www.ryans.com/category/all-laptop-apple",
            "https://www.ryans.com/category/smart-phone-apple",
            "https://www.ryans.com/category/apple-tablet-ipad",
            "https://www.ryans.com/category/mini-pc-apple",
            "https://www.ryans.com/category/smartwatch-apple",
            "https://www.ryans.com/search?search=Apple+iMac",
            "https://www.ryans.com/category/earphone-airpods",
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
                    page.wait_for_selector('.category-single-product', timeout=10000)
                    html = page.content()
                    soup = BeautifulSoup(html, "html.parser")
                    products = soup.find_all("div", class_="category-single-product")

                    for product in products:
                        try:
                            name_el = product.find(class_="card-text")
                            for span in name_el.find_all("span"):
                                span.decompose()
                            name = name_el.get_text(strip=True)
                            price_text = product.find(class_="pr-text").get_text(strip=True)
                            price = float(price_text.replace("Tk", "").replace(",", "").strip())
                            results.append(self.format_result(name, price))
                        except Exception:
                            continue

                except Exception as e:
                    print(f"[ryans] failed for {url}: {e}")

            browser.close()

        return results