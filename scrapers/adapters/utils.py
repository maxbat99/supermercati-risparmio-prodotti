from __future__ import annotations
from bs4 import BeautifulSoup as BS
import requests
from urllib.parse import urljoin

def find_pdf_links(page_url: str, keywords=("volantino","offerta","promo","sfoglia","pdf")):
    r = requests.get(page_url, timeout=30, headers={"User-Agent":"Mozilla/5.0"})
    r.raise_for_status()
    soup = BS(r.text, "lxml")
    out = []
    for a in soup.select("a[href]"):
        href = a["href"]
        low = href.lower()
        if href.lower().endswith(".pdf") and any(k in low for k in keywords):
            out.append(urljoin(page_url, href))
    # unique preserve order
    seen=set(); ret=[]
    for u in out:
        if u not in seen:
            seen.add(u); ret.append(u)
    return ret
