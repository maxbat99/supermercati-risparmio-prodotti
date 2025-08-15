from __future__ import annotations
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup as BS

def scrape_dynamic(url: str, item_selector: str, name_sel: str, price_sel: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers({"User-Agent":"Mozilla/5.0"})
        page.goto(url, wait_until="networkidle")
        html = page.content()
        browser.close()
    soup = BS(html, "lxml")
    items = []
    for card in soup.select(item_selector):
        name = (card.select_one(name_sel).get_text(strip=True) if card.select_one(name_sel) else None)
        price = (card.select_one(price_sel).get_text(strip=True) if card.select_one(price_sel) else None)
        if not name or not price: 
            continue
        # estrazione numerica semplice "€ 1,99" -> 1.99
        import re
        m = re.search(r"([0-9]+[\\.,][0-9]{1,2})", price)
        if not m: 
            continue
        val = float(m.group(1).replace(",", "."))
        items.append({"name_raw": name, "price": val, "source_type":"site"})
    return items
