from .utils import find_pdf_links
from ..common import http_get, extract_pdf_text, parse_offers_text
CHAIN="MD"
def scrape(store_url: str):
    offers=[]
    for pdf in find_pdf_links(store_url):
        txt = extract_pdf_text(http_get(pdf))
        for o in parse_offers_text(txt):
            o.update({"chain":CHAIN,"source_url":pdf,"source_type":"leaflet"})
            offers.append(o)
    return offers
