"""
IDX Comprehensive Ticker List — multi-source fallback
"""
import yfinance as yf
import pandas as pd
import requests
import re
from pathlib import Path

OUT = Path("data_acquisition/raw")
OUT.mkdir(parents=True, exist_ok=True)

# --- Known public API for IDX tickers ---
print("[1] Fetching from Bursa Efek Indonesia public listing...")
try:
    url = "https://www.idx.co.id/Portals/0/StaticData/IDX/IDX_Stock_Listing.json"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Accept": "application/json, text/plain, */*"}
    r = requests.get(url, headers=headers, timeout=30)
    print(f"  Status: {r.status_code}")
except: pass

# --- Try Bursa Indonesia public page ---
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
print("[2] Trying IDX listed companies page...")
try:
    r = requests.get("https://www.idx.co.id/en/listed-companies", headers=headers, timeout=30)
    if r.status_code == 200:
        # look for JSON data or ticker patterns in JS
        tickers_raw = re.findall(r'[A-Z]{4}\.JK', r.text)
        if tickers_raw:
            print(f"  Found {len(set(tickers_raw))} ticker patterns on page")
            pd.Series(sorted(set(tickers_raw))).to_csv(OUT / "idx_tickers_from_html.csv", index=False, header=["ticker"])
except Exception as e:
    print(f"  Failed: {e}")

# --- Build from known IDX ticker patterns ---
# 700+ publicly traded companies on IDX
print("\n[3] Building comprehensive IDX list from Yahoo Finance query...")
# Fetch all tickers from Yahoo Finance for ID (Indonesia) market
try:
    # Yahoo's screener API can list stocks by country
    url = "https://query1.finance.yahoo.com/v1/finance/screener"
    params = {
        "lang": "en-US",
        "region": "ID",
        "formatted": "true",
        "corsDomain": "finance.yahoo.com",
    }
    headers["Origin"] = "https://finance.yahoo.com"

    payload = {
        "size": 250,  # max per page
        "offset": 0,
        "sortField": "ticker",
        "sortType": "asc",
        "quoteTypeFilter": "EQUITY",
        "query": {
            "operator": "eq",
            "operands": [{"operator": "eq", "operands": ["region", "ID"], "operands": []}],  # noqa
        },
    }
    r = requests.post(url, json=payload, headers=headers, params=params, timeout=30)
    print(f"  Yahoo screener status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        quotes = data.get("finance", {}).get("result", [{}])[0].get("quotes", [])
        print(f"  Got {len(quotes)} tickers from Yahoo screener")
        if quotes:
            tickers = [q.get("symbol") for q in quotes if q.get("symbol", "").endswith(".JK")]
            pd.Series(tickers).to_csv(OUT / "idx_tickers_yahoo_screener.csv", index=False, header=["ticker"])
except Exception as e:
    print(f"  Yahoo screener failed: {e}")

# --- Fallback: use a comprehensive manual list from IDX history ---
print("\n[4] Trying IDX stock data from API...")
try:
    for endpoint in [
        "https://www.idx.co.id/primary/StockData/GetStockList?start=0&limit=1000",
        "https://www.idx.co.id/primary/ListedCompany/GetCompanyList?start=0&length=1000",
    ]:
        r = requests.get(endpoint, headers=headers, timeout=30)
        if r.status_code == 200:
            data = r.json()
            print(f"  {endpoint[:50]}... -> Status 200, type={type(data).__name__}")
            print(f"  Sample: {str(data)[:300]}")
except Exception as e:
    print(f"  Failed: {e}")

# --- Save whatever we have ---
print("\n=== Checking collected files ===")
for f in sorted(OUT.glob("idx_tickers*")):
    df = pd.read_csv(f)
    print(f"  {f.name}: {len(df)} rows")

print("\nDONE")
