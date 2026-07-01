"""
Download IDX financial data — price, fundamental, macro
Produces the core panel dataset for the Data Descriptor
"""
import yfinance as yf
import pandas as pd
import numpy as np
from pathlib import Path
import time, os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

OUT = Path("data_acquisition/raw")
OUT.mkdir(parents=True, exist_ok=True)

VALIDATED = OUT / "idx_tickers_validated.csv"
if not VALIDATED.exists():
    print("❌ Run 03_build_ticker_list.py first")
    exit(1)

df_tickers = pd.read_csv(VALIDATED)
tickers = [f"{t}.JK" for t in df_tickers["ticker"].tolist()]
print(f"📊 Loading data for {len(tickers)} tickers...")

# ========== STOCK PRICE DATA ==========
print("\n📈 Downloading stock price data (2010-01-01 to 2025-12-31)...")
all_prices = []
failed = 0
for i, t in enumerate(tickers):
    try:
        d = yf.download(t, start="2010-01-01", end="2026-12-31", progress=False, auto_adjust=True)
        if len(d) > 0:
            d.columns = [str(c[0]) if isinstance(c, tuple) else str(c) for c in d.columns]
            d = d.reset_index()
            d["ticker"] = t.replace(".JK", "")
            date_col = [c for c in d.columns if "date" in str(c).lower()]
            if date_col:
                d = d.rename(columns={date_col[0]: "date"})
            for col in ["Open","High","Low","Close","Volume"]:
                if col in d.columns:
                    d[col] = d[col].astype(float).round(2)
            all_prices.append(d)
        print(f"  [{i+1}/{len(tickers)}] {t:12s} -> {len(d):>5d} days", end="\r")
    except Exception as e:
        failed += 1
    time.sleep(0.15)

print(f"\n✅ Downloaded {len(all_prices)}/{len(tickers)} tickers ({failed} failed)")
if all_prices:
    prices_df = pd.concat(all_prices, ignore_index=True)
    prices_df.columns = [str(c).lower() for c in prices_df.columns]
    prices_df = prices_df.sort_values(["ticker", "date"])
    prices_df.to_csv(OUT / "idx_stock_prices.csv", index=False)
    print(f"   Saved: {len(prices_df):,} rows x {len(prices_df.columns)} cols")
    print(f"   Date range: {prices_df['date'].min()} to {prices_df['date'].max()}")

# ========== SIMULATED FUNDAMENTAL DATA ==========
# yfinance has limited fundamental data for IDX stocks via info
# We extract what's available
print("\n📊 Extracting fundamental data from yfinance info...")
fundamentals = []
for i, ticker in enumerate(tickers):
    try:
        t = yf.Ticker(ticker)
        info = t.info
        if info and info.get("marketCap"):
            fundamentals.append({
                "ticker": ticker.replace(".JK", ""),
                "name": info.get("longName", ""),
                "sector": info.get("sector", ""),
                "industry": info.get("industry", ""),
                "marketCap": info.get("marketCap"),
                "enterpriseValue": info.get("enterpriseValue", np.nan),
                "trailingPE": info.get("trailingPE", np.nan),
                "forwardPE": info.get("forwardPE", np.nan),
                "priceToBook": info.get("priceToBook", np.nan),
                "returnOnEquity": info.get("returnOnEquity", np.nan),
                "returnOnAssets": info.get("returnOnAssets", np.nan),
                "debtToEquity": info.get("debtToEquity", np.nan),
                "revenueGrowth": info.get("revenueGrowth", np.nan),
                "earningsGrowth": info.get("earningsGrowth", np.nan),
                "dividendYield": info.get("dividendYield", np.nan),
                "payoutRatio": info.get("payoutRatio", np.nan),
                "beta": info.get("beta", np.nan),
                "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh", np.nan),
                "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow", np.nan),
                "currency": info.get("currency", ""),
            })
        print(f"  [{i+1}/{len(tickers)}] {ticker:12s} -> OK", end="\r")
    except:
        pass
    time.sleep(0.1)

if fundamentals:
    fund_df = pd.DataFrame(fundamentals)
    fund_df.to_csv(OUT / "idx_fundamentals.csv", index=False)
    print(f"\n✅ Saved {len(fund_df)} company fundamentals")

# ========== MACRO DATA (via fixed sources) ==========
print("\n🏦 Creating macro-economic framework template...")
macro_years = list(range(2010, 2026))
macro_data = pd.DataFrame({
    "year": macro_years,
    # These will need manual filling from BI & BPS sources
    # We document the source structure here
    "bi_rate_pct": np.nan,       # Source: www.bi.go.id
    "inflation_pct": np.nan,      # Source: www.bps.go.id
    "gdp_growth_pct": np.nan,     # Source: www.bps.go.id
    "usd_idr_rate": np.nan,       # Source: Bank Indonesia
    "ihsg_close": np.nan,         # Source: IDX / Yahoo ^JKSE
})
macro_data.to_csv(OUT / "idx_macro_template.csv", index=False)
print(f"   Saved macro template ({len(macro_years)} years)")

# Download IHSG index
print("\n📉 Downloading IHSG index (^JKSE) for reference...")
try:
    ihsg = yf.download("^JKSE", start="2010-01-01", end="2026-12-31", progress=False, auto_adjust=True)
    if len(ihsg) > 0:
        ihsg.to_csv(OUT / "idx_ihsg_index.csv")
        print(f"   Downloaded {len(ihsg)} days of IHSG data")
except Exception as e:
    print(f"   IHSG download failed: {e}")

print("\n" + "="*50)
print("✅ DATA ACQUISITION COMPLETE")
print("="*50)
for f in sorted(OUT.glob("idx_*")):
    sz = f.stat().st_size / 1024
    print(f"  📄 {f.name:45s} {sz:>8.1f} KB")
