"""
Build IDX ticker list by scanning known patterns via yfinance
IDX tickers format: [A-Z]{2,4}.JK
We use multiple strategies to build the list.
"""
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time

OUT = Path("data_acquisition/raw")
OUT.mkdir(parents=True, exist_ok=True)

# --- Strategy 1: Scrape known sources for IDX company list ---
print("[1] Scraping Bursa Efek Indonesia listing page...")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}
try:
    r = requests.get("https://www.idx.co.id/en/listed-companies/", headers=headers, timeout=30)
    print(f"  IDX page status: {r.status_code}")
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text()
        # Find stock code patterns (typically 1-4 uppercase letters)
        import re
        # IDX tickers are 1-4 letters code followed by stock name
        # Common in tables
        found_tickers = set()
        for match in re.finditer(r'\b([A-Z]{2,4})\s+(?:PT\s+|Tbk)', text):
            found_tickers.add(match.group(1))
        print(f"  Found {len(found_tickers)} potential tickers")
        if found_tickers:
            pd.Series(sorted(found_tickers)).to_csv(OUT / "idx_tickers_scraped.csv", index=False, header=["ticker"])
except Exception as e:
    print(f"  Failed: {e}")

# --- Strategy 2: Use TradingView screener endpoint (public) ---
print("\n[2] Using TradingView screener for IDX stocks...")
try:
    headers["Origin"] = "https://id.tradingview.com"
    # TradingView screener query for IDX
    payload = {
        "symbols": {"query": {"types": ["stock"]}, "tickers": [], "groups": [{"type": "market", "value": "IDX"}]},
        "columns": ["name", "close", "market_cap_basic", "sector"],
        "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"},
        "range": [0, 500],
    }
    r = requests.post(
        "https://scanner.tradingview.com/indonesia/scan",
        json=payload,
        headers={"User-Agent": headers["User-Agent"], "Content-Type": "application/json"},
        timeout=30,
    )
    if r.status_code == 200:
        data = r.json()
        symbols = [d["s"] for d in data.get("data", [])]
        print(f"  Got {len(symbols)} symbols")
        if symbols:
            pd.Series(symbols).to_csv(OUT / "idx_tickers_tradingview.csv", index=False, header=["ticker"])
except Exception as e:
    print(f"  TradingView failed: {e}")

# --- Strategy 3: Use investing.com IDX stocks ---
print("\n[3] Fetching from Investing.com Indonesia stocks...")
try:
    url = "https://www.investing.com/equities/indonesia"
    r = requests.get(url, headers=headers, timeout=30)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text()
        tickers = set(re.findall(r'\b([A-Z]{2,4})\.JK\b', text))
        print(f"  Found {len(tickers)} .JK tickers")
        if tickers:
            pd.Series(sorted(tickers)).to_csv(OUT / "idx_tickers_investing.csv", index=False, header=["ticker"])
except Exception as e:
    print(f"  Failed: {e}")

# --- Strategy 4: Direct yfinance validation of known IDX stocks ---
print("\n[4] Validating known major IDX stocks via yfinance...")
# Build from industry lists
import os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')  # noqa

MAJOR_TICKERS = [
    # Financials
    "BBRI", "BMRI", "BBCA", "BBNI", "BDMN", "BNGA", "BNLI", "NISP", "MAYA", "BNII",
    "AGRO", "BJBR", "BJTM", "BSIM", "BTPN", "INPC", "MEGA", "SDRA", "NOBU", "PNBN",
    # Consumer
    "UNVR", "HMSP", "GGRM", "ICBP", "INDF", "MYOR", "ROTI", "SKLT", "ULTJ", "DLTA",
    "MLBI", "STTP", "CEKA", "ADES", "CLEO", "BUDI", "ALTO", "PANI",
    # Mining & Energy
    "ADRO", "PTBA", "ANTM", "ITMG", "HRUM", "INDY", "MEDC", "PGAS", "ELSA", "SMMT",
    # Infrastructure
    "TLKM", "EXCL", "JSMR", "ISAT", "TOWR", "TBIG", "FREN", "BALI",
    # Industrial
    "ASII", "KBLM", "BOLT", "INDS", "GJTL", "CTRA", "PWON", "BSDE", "LPKR", "SMRA",
    "TIFA", "TURI", "BKSL", "LPCK", "RIJK",
    # Basic Materials
    "SMGR", "WTON", "WSKT", "WSBP", "TKIM", "INKP", "INRU", "TINS", "BRMS",
    # Healthcare
    "KLBF", "KAEF", "DVLA", "TSPC", "SIDO", "MERK", "PYFA",
    # Technology
    "MTDL", "MLPT", "POWR", "EMTK", "BUKA", "GOTO",
    # Property
    "LPKR", "BSDE", "CTRA", "ADHI", "PTPP", "WIKA", "TOTL", "ACST",
]

valid = []
for t in MAJOR_TICKERS:
    jk = f"{t}.JK"
    try:
        _t = yf.Ticker(jk)
        info = _t.info
        if info and info.get("longName") and info.get("marketCap", 0) > 0:
            valid.append({
                "ticker": t,
                "yahoo_ticker": jk,
                "name": info.get("longName", ""),
                "sector": info.get("sector", ""),
                "industry": info.get("industry", ""),
                "marketCap": info.get("marketCap", 0),
                "currency": info.get("currency", ""),
            })
            print(f"  ✓ {jk} -> {info.get('sector',''):20s} | {info.get('longName','')[:50]}")
        else:
            print(f"  ✗ {jk} -> invalid")
    except Exception as e:
        print(f"  ✗ {jk} -> {str(e)[:40]}")
    time.sleep(0.1)  # rate limit

df = pd.DataFrame(valid)
if len(df) > 0:
    df.to_csv(OUT / "idx_tickers_validated.csv", index=False)
    print(f"\n✅ Validated {len(df)} tickers")
    print(f"   Sectors: {df['sector'].nunique()} unique")
    print(f"   MCAP range: {df['marketCap'].min():,.0f} - {df['marketCap'].max():,.0f}")
else:
    print("\n❌ No valid tickers found")

print("\nDONE")
