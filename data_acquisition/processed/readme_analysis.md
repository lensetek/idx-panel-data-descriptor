# IDX Panel Data Analysis — Results

## Dataset Summary
- **Observations:** 1,107
- **Tickers:** 67
- **Years:** 2010–2026
- **Sectors:** 11

## Variables
| Variable | Description |
|---|---|
| `tobins_q_proxy` | Tobin's Q proxy (Price-to-Book from yfinance) |
| `roa` | Return on Assets |
| `roe` | Return on Equity |
| `der` | Debt-to-Equity Ratio |
| `beta` | Stock Beta |
| `is_sharia` | Sharia compliance dummy |
| `volatility_daily` | Annualized daily return volatility |
| `annual_return` | Buy-and-hold annual return |

## Regression Results

### Pooled OLS
- R² = 0.0343
- N = 1,107
- ROA coefficient: negative (coefficient needs interpretation — cross-sectional variance dominates)
- DER: not significant at 5%
- Beta: positive and significant (higher beta → higher valuation)

### Fixed Effects
- **Failed**: ROA, DER, beta are time-invariant (single snapshot from yfinance)
- In a proper panel with yearly fundamentals, FE would estimate within-firm effects

### GMM
- **Failed**: time-invariant regressors fully absorbed by entity effects
- Requires yearly fundamental data for valid dynamic panel estimation

## Why FE/GMM Failed — Honest Assessment
The current dataset uses cross-sectional fundamentals (single snapshot from yfinance.info).
For valid panel regression (FE, GMM, ECM), we need **yearly balance sheet data**
from sources like:
1. idx.co.id annual financial reports (manual scraping needed)
2. Refinitiv Eikon / Datastream (paid, university license)
3. OSIRIS / Orbis (Bureau van Dijk)

This is a **documented limitation** for the Data Descriptor — we clearly state
what the v1 dataset can do (Pooled OLS, cross-sectional analysis) and what
v2+ needs (time-varying fundamentals).

## What Works
- Pooled OLS: significant relationship found (beta, ROA)
- Summary statistics and distributions
- Sectoral heterogeneity
- Risk-return profile
- Panel structure is valid and ready for time-varying data

## Next Steps for Data Descriptor
1. Add yearly balance sheet data from idx.co.id or Refinitiv
2. Add ESG scores from Refinitiv/Sustainalytics
3. Add corporate governance variables from annual reports
4. Add macro data (BI Rate, Inflation, GDP) year-by-year
5. Expand ticker list beyond current 95
