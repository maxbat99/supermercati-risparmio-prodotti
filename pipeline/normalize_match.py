from __future__ import annotations
import re
_qty = re.compile(r"(\\d+[\\.,]?\\d*)\\s*(kg|g|l|ml|pz|x\\s*\\d+\\s*\\w+)", re.I)
def infer_qty_unit(name_or_qty: str|None):
    if not name_or_qty: return None, None
    m = _qty.search(name_or_qty)
    if not m: return None, None
    qty = float(m.group(1).replace(",", "."))
    unit = m.group(2).lower()
    if unit == "g": qty /= 1000
    if unit == "ml": qty /= 1000
    return qty, ("kg" if unit in ("kg","g") else "l" if unit in ("l","ml") else "pz")
def unit_price(price: float, qty: float|None):
    if qty is None or qty <= 0: return None
    return round(price / qty, 2)
