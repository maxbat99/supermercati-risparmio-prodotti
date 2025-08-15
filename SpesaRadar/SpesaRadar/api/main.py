from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

app = FastAPI(title="SpesaRadar API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True)

class Offer(BaseModel):
    id: str
    canonical_id: str
    product_name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[str] = None
    unit_price: Optional[float] = None
    price: float
    currency: str = "EUR"
    discount_pct: Optional[float] = None
    valid_from: date
    valid_to: date
    chain: str
    store_city: str
    store_address: Optional[str] = None
    source_url: Optional[str] = None
    source_type: str

class OfferPage(BaseModel):
    items: List[Offer]
    total: int
    page: int
    page_size: int

DATA = [
    {
        "id": "md-001",
        "canonical_id": "pasta_barilla_spaghetti_500g",
        "product_name": "Spaghetti n.5 Barilla 500 g",
        "brand": "Barilla",
        "category": "Pasta",
        "quantity": "500 g",
        "unit_price": 2.18,
        "price": 1.09,
        "currency": "EUR",
        "discount_pct": 30.0,
        "valid_from": date(2025, 8, 14),
        "valid_to": date(2025, 8, 21),
        "chain": "MD",
        "store_city": "Torre del Greco",
        "store_address": "Via Nazionale 123",
        "source_url": "#",
        "source_type": "leaflet",
    },
]

@app.get("/health")
def health():
    return {"status": "ok", "now": datetime.utcnow().isoformat()}

@app.get("/cities", response_model=List[str])
def cities():
    return sorted(list({o["store_city"] for o in DATA}))

@app.get("/chains", response_model=List[str])
def chains():
    return sorted(list({o["chain"] for o in DATA}))

@app.get("/offers", response_model=OfferPage)
def offers(
    city: Optional[str] = None,
    chain: Optional[str] = None,
    q: Optional[str] = None,
    category: Optional[str] = None,
    sort: str = Query("unit_price", pattern="^(price|unit_price|discount)$"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    valid_on: Optional[date] = None,
    page: int = 1,
    page_size: int = 24,
):
    items = DATA.copy()

    def like(s: str, sub: str) -> bool:
        return sub.lower() in (s or "").lower()

    if city:
        items = [o for o in items if o["store_city"].lower() == city.lower()]
    if chain:
        items = [o for o in items if o["chain"].lower() == chain.lower()]
    if q:
        items = [o for o in items if like(o["product_name"], q) or like(o.get("brand"), q)]
    if category:
        items = [o for o in items if o.get("category") and o["category"].lower() == category.lower()]
    if valid_on:
        items = [o for o in items if o["valid_from"] <= valid_on <= o["valid_to"]]

    reverse = order == "desc"
    items.sort(key=lambda o: (o.get(sort) is None, o.get(sort, 0)), reverse=reverse)

    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    page_items = [Offer(**o) for o in items[start:end]]

    return OfferPage(items=page_items, total=total, page=page, page_size=page_size)

@app.get("/products/{canonical_id}/offers", response_model=List[Offer])
def offers_by_canonical(canonical_id: str):
    rows = [Offer(**o) for o in DATA if o["canonical_id"] == canonical_id]
    if not rows:
        raise HTTPException(404, "Nessuna offerta trovata per questo prodotto")
    return sorted(rows, key=lambda o: (o.unit_price is None, o.unit_price or 0))
