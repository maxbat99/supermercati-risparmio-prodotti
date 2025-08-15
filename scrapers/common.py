from __future__ import annotations
import re, requests
from pdf2image import convert_from_bytes
import pytesseract

UA = {"User-Agent":"Mozilla/5.0"}

def http_get(url: str, timeout: int = 30) -> bytes:
    r = requests.get(url, timeout=timeout, headers=UA)
    r.raise_for_status()
    return r.content

def extract_pdf_text(pdf_bytes: bytes) -> str:
    images = convert_from_bytes(pdf_bytes, dpi=200)
    parts = []
    for img in images:
        parts.append(pytesseract.image_to_string(img, lang="ita+eng"))
    return "\n".join(parts)

_price = re.compile(r"(?:€|EUR)\\s*([0-9]+[\\.,][0-9]{1,2})")
_qty = re.compile(r"(\\d+[\\.,]?\\d*)\\s*(kg|g|l|ml|pz|x\\s*\\d+\\s*\\w+)", re.I)

def parse_offers_text(text: str):
    out = []
    blocks = [b.strip() for b in re.split(r"\\n\\s*\\n", text) if b.strip()]
    for b in blocks:
        m = _price.search(b.replace(",", "."))
        if not m: 
            continue
        price = float(m.group(1))
        head = b.splitlines()[0][:120]
        qm = _qty.search(b)
        qty = qm.group(0) if qm else None
        out.append({"name_raw": head, "quantity_raw": qty, "price": price})
    return out
