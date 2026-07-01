"""
IDX Ticker Collector — fetch all IDX-listed stocks from Yahoo Finance
using sector/market data and IDX official sources.
"""
import yfinance as yf
import pandas as pd
import requests
import json
from pathlib import Path

OUT = Path("data_acquisition/raw")
OUT.mkdir(parents=True, exist_ok=True)

# --- METHOD 1: Known IDX tickers (comprehensive list via Wikipedia/IDX) ---
print("[1] Fetching IDX stock list from Wikipedia...")
try:
    tables = pd.read_html("https://en.wikipedia.org/wiki/List_of_companies_listed_on_the_Indonesia_Stock_Exchange")
    # The first table usually contains the listing
    idx_list = tables[0]
    idx_list.to_csv(OUT / "idx_companies_wikipedia.csv", index=False)
    print(f"  -> Saved {len(idx_list)} companies from Wikipedia")
except Exception as e:
    print(f"  WARNING: Wikipedia fetch failed: {e}")

# --- METHOD 2: Yahoo Finance sector scan ---
# Common IDX banks & large caps as seed tickers
SEED_TICKERS = [
    "BBRI.JK", "BMRI.JK", "BBCA.JK", "BBNI.JK", "TLKM.JK",
    "ASII.JK", "UNVR.JK", "ADRO.JK", "GGRM.JK", "HMSP.JK",
    "ICBP.JK", "INDF.JK", "KLBF.JK", "SMGR.JK", "PTBA.JK",
    "EXCL.JK", "JSMR.JK", "PGAS.JK", "ANTM.JK", "CTRA.JK",
]

# If we had a comprehensive list from Wikipedia, supplement it
# For now, scan Yahoo Finance for IDX tickers using industry peers

print("\n[2] Fetching seed ticker data from Yahoo Finance...")
seed_info = []
for t in SEED_TICKERS:
    try:
        ticker = yf.Ticker(t)
        info = ticker.info
        if info and info.get("longName"):
            seed_info.append({
                "ticker": t,
                "name": info.get("longName", ""),
                "sector": info.get("sector", ""),
                "industry": info.get("industry", ""),
                "marketCap": info.get("marketCap", 0),
            })
            print(f"  OK: {t} - {info.get('sector', 'N/A')}")
    except Exception as e:
        print(f"  FAIL: {t} - {e}")

seed_df = pd.DataFrame(seed_info)
seed_df.to_csv(OUT / "idx_seed_tickers_yahoo.csv", index=False)
print(f"\nCollected {len(seed_df)} seed tickers with sector info")

# --- METHOD 3: Build comprehensive ticker list from IDX official ---
print("\n[3] Fetching IDX listed companies from IDX official API...")
try:
    # IDX provides stock data through their API
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }
    # IDX stock listing endpoint (public)
    url = "https://www.idx.co.id/Portals/0/StaticData/IDX/IDX_Stock_Listing.json"
    resp = requests.get(url, headers=headers, timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        # IDX sometimes serves this differently, check structure
        print(f"  IDX API returned: {type(data).__name__}")
        print(f"  Sample: {str(data)[:200]}")
    else:
        print(f"  IDX API returned status {resp.status_code}")
except Exception as e:
    print(f"  WARNING: IDX API failed: {e}")

# Alternative: IDX stock data via BEI public listing
try:
    url2 = "https://www.idx.co.id/primary/StockData/GetStockList"
    resp2 = requests.get(url2, headers=headers, timeout=30)
    if resp2.status_code == 200:
        data2 = resp2.json()
        print(f"  IDX StockList returned: {type(data2).__name__}")
        with open(OUT / "idx_stock_list_raw.json", "w") as f:
            json.dump(data2, f, indent=2)
        print("  Saved to idx_stock_list_raw.json")
except Exception as e:
    print(f"  Alternative IDX API also failed: {e}")

print("\n=== TICKER COLLECTION COMPLETE ===")
print("Seed tickers saved to:", OUT / "idx_seed_tickers_yahoo.csv")
print("Wikipedia table saved to:", OUT / "idx_companies_wikipedia.csv")
