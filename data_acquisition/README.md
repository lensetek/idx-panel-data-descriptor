# IDX Panel Dataset (2010–2026)

A curated panel dataset of the Indonesia Stock Exchange covering 67 major non-financial firms from 2010 to 2026.

## Summary

- **Daily prices**: 373,577 observations across 95 tickers
- **Panel**: 1,107 firm-year observations (67 tickers, 17 years)
- **Variables**: Stock returns, volatility, Tobin's Q proxy (PBV), ROA, ROE, DER, Beta, market cap, Sharia compliance
- **Sectors**: Basic Materials, Consumer Cyclical, Consumer Defensive, Energy, Healthcare, Industrials, Real Estate, Technology, Communication Services, Utilities
- **Source**: Yahoo Finance (yfinance Python library)
- **License**: CC-BY 4.0

## Files

| File | Description |
|---|---|
| `idx_stock_prices.csv` | Daily OHLCV data (373,577 rows) |
| `idx_fundamentals.csv` | Firm-level financial fundamentals (98 companies) |
| `panel_master.csv` | Firm-year panel dataset (1,107 rows) — primary analysis file |
| `idx_ihsg_index.csv` | Jakarta Composite Index daily data |
| `idx_tickers_validated.csv` | Validated ticker list with sector metadata |
| `codebook.md` | Full variable dictionary |

## Quick Start

```python
import pandas as pd

# Load the panel
df = pd.read_csv("panel_master.csv")

# Basic summary
print(df.groupby("year")["tobins_q_proxy"].mean())

# Regression (see validation_script.py in repo for full pipeline)
import statsmodels.api as sm
X = sm.add_constant(df[["roa", "der", "beta"]])
model = sm.OLS(df["tobins_q_proxy"], X).fit(cov_type="HC3")
print(model.summary())
```

## Important Limitations (v1)

- **Cross-sectional fundamentals**: ROA, ROE, DER, Beta are single-snapshot values (not time-varying). Fixed-effects and GMM panel models cannot be estimated. See manuscript for v2 roadmap.
- **Coverage**: 67 firms (~7% of IDX listings by count), concentrated among large-cap names
- **Sharia classification**: Sector-level proxy. Firm-level DES data planned for v2.
- **No ESG or governance variables**: Deferred to v2.

## Citation

If you use this dataset, please cite:

> Kesuma, A. & Ismail, A. A Panel Dataset of the Indonesia Stock Exchange: Prices, Fundamentals, and Sharia Classification (2010–2026). *Scientific Data* (under review). Zenodo. doi:[to be assigned]

## Contact

- Ali Kesuma — ali@unda.ac.id
- Andy Ismail — andy@unda.ac.id
- Faculty of Business, Universitas Darwan Ali, Indonesia

## Repository

Source code and documentation: https://github.com/lensetek/idx-panel-data-descriptor
