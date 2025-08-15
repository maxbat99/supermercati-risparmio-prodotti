from __future__ import annotations
import importlib, json, yaml, pathlib, datetime as dt
from pipeline.normalize_match import infer_qty_unit, unit_price

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "scrapers" / "registry.yml"
OUT = ROOT / "data" / "offers.json"

def run():
    reg = yaml.safe_load(REG.read_text(encoding="utf-8"))
    items = []
    for chain, cfg in reg.get("chains", {}).items():
        adapter = cfg["adapter"]
        mod = importlib.import_module(f"scrapers.adapters.{adapter}")
        # per dynamic_html passiamo i selettori dal registry
        conf = cfg.get("config", {})
        for s in cfg.get("stores", []):
            url = s["url"]; city = s.get("city","")
            try:
                if adapter == "dynamic_html":
                    rows = mod.scrape_dynamic(url, conf["item_selector"], conf["name_selector"], conf["price_selector"])
                else:
                    rows = mod.scrape(url)
            except Exception as e:
                print(f"[WARN] {chain} {city}: {e}")
                continue
            for r in rows:
                q, u = infer_qty_unit(r.get("quantity_raw") or r.get("name_raw"))
                up = unit_price(r["price"], q)
                items.append({
                    "id": f"{chain}-{abs(hash((r.get('name_raw') or '')+str(r['price'])+city))}",
                    "canonical_id": (r.get("name_raw") or "").lower().replace(" ","_")[:64],
                    "product_name": r.get("name_raw") or "",
                    "brand": None,
                    "category": None,
                    "quantity": r.get("quantity_raw"),
                    "unit_price": up,
                    "price": round(float(r["price"]),2),
                    "currency": "EUR",
                    "discount_pct": None,
                    "valid_from": str(dt.date.today()),
                    "valid_to": str(dt.date.today()+dt.timedelta(days=7)),
                    "chain": chain.capitalize(),
                    "store_city": city,
                    "store_address": None,
                    "source_url": r.get("source_url") or url,
                    "source_type": r.get("source_type","site")
                })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(items)} → {OUT}")

if __name__ == "__main__":
    run()
