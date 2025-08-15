from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Offer(BaseModel):
    id: str; product_name: str; chain: str
    store_city: Optional[str] = None; store_address: Optional[str] = None
    price: float; unit_price: Optional[float] = None
    discount_pct: Optional[int] = None
    valid_from: Optional[date] = None; valid_to: Optional[date] = None

DEMO: List[Offer] = [
    Offer(id="1", product_name="Latte Intero 1L", chain="MD", store_city="Portici", store_address="Corso Garibaldi 50", price=1.09, unit_price=1.09),
    Offer(id="2", product_name="Latte Intero 1L", chain="Conad", store_city="Torre del Greco", store_address="Via Nazionale 12", price=1.19, unit_price=1.19),
]

@app.get("/health") 
def health(): return {"status":"ok"}

@app.get("/cities") 
def cities(): return sorted({o.store_city for o in DEMO if o.store_city})

@app.get("/chains") 
def chains(): return sorted({o.chain for o in DEMO if o.chain})

@app.get("/offers")
def offers(q: Optional[str] = None):
    items = DEMO
    if q: items = [o for o in items if q.lower() in o.product_name.lower()]
    return {"items": items, "total": len(items), "page": 1, "page_size": len(items)}
