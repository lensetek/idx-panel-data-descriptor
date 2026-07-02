# IDX Panel Dataset (2010–2026)

A curated panel dataset of the Indonesia Stock Exchange (IDX) covering 67 major non-financial firms from 2010 to 2026, with daily stock prices, annual financial fundamentals, and Sharia classification.

This repository hosts the **data acquisition pipeline, validation scripts, and manuscript** for a Data Descriptor submitted to *Scientific Data* (Nature).

**Authors**: Ali Kesuma (ali@unda.ac.id), Andy Ismail (andy@unda.ac.id) — Faculty of Business, Universitas Darwan Ali, Indonesia

**DOI**: [10.5281/zenodo.21110404](https://zenodo.org/records/21110404)

---

## Dataset

### Summary

| Metric | Value |
|---|---|
| Daily price observations | 373,577 rows (95 tickers) |
| Panel (firm-year) | 1,107 obs (67 tickers, 17 years) |
| Time span | 4 Jan 2010 – 1 Jul 2026 |
| Fundamentals | Cross-sectional (single snapshot) |
| Sectors | 10 non-financial sectors |
| License | CC-BY 4.0 |

### Files

| File | Description |
|---|---|
| `data_acquisition/raw/idx_stock_prices.csv` | Daily OHLCV for 95 IDX tickers |
| `data_acquisition/raw/idx_fundamentals.csv` | Financial ratios & market cap (98 firms) |
| `data_acquisition/raw/idx_ihsg_index.csv` | Jakarta Composite Index (IHSG), daily |
| `data_acquisition/raw/idx_tickers_validated.csv` | Ticker list with sector & market cap |
| `data_acquisition/processed/panel_master.csv` | **Primary analysis file** — firm-year panel with returns, volatility, Tobin's Q, ROA, ROE, DER, Beta, Sharia flag |
| `data_acquisition/processed/regression_results.csv` | All model coefficients (OLS, FE, RE, GMM) |
| `data_acquisition/codebook.md` | Full variable dictionary |

### Variables (panel_master.csv)

- **Return**: Mean & median daily log return (annual), annual buy-and-hold return
- **Risk**: Annual volatility (standard deviation of daily returns)
- **Valuation**: Tobin's Q proxy (Price-to-Book Value ratio)
- **Fundamentals**: ROA, ROE, Debt-to-Equity Ratio, Beta, market capitalization
- **Sharia**: Binary flag based on sector-level screening (10 non-financial sectors)
- **Trading**: Annual average trading volume

See [`data_acquisition/codebook.md`](data_acquisition/codebook.md) for full details.

---

## Pipeline

Reproducible Python pipeline (run sequentially):

```
01_get_tickers.py      → Scrape IDX tickers from Wikipedia, Yahoo, IDX API
02_get_all_tickers.py  → Multi-source fallback (Yahoo screener, TradingView)
03_build_ticker_list.py→ Validate ~100 tickers via yfinance
04_download_data.py    → Download OHLCV prices + fundamentals + IHSG index
05_panel_regression.py → Returns → annual aggregation → merge → panel models + summary stats
06_validation.py       → OLS diagnostics: Jarque-Bera, BP, VIF, DW, Chow, HC3 SE
```

### Requirements

Python 3.11+ with: `yfinance`, `pandas`, `numpy`, `statsmodels`, `linearmodels`, `scipy`, `matplotlib`, `seaborn`, `requests`, `beautifulsoup4`.

### Quick Start

```python
import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("data_acquisition/processed/panel_master.csv")

# Pooled OLS with HC3 robust SE (the validated specification)
X = sm.add_constant(df[["roa", "der", "beta"]])
y = df["tobins_q_proxy"]
model = sm.OLS(y, X).fit(cov_type="HC3")
print(model.summary())
```

---

## Important Limitations (v1)

- **Cross-sectional fundamentals**: ROA, ROE, DER, Beta are single-snapshot values from Yahoo Finance. Fixed-effects and Arellano-Bond GMM cannot be estimated — entity effects perfectly absorb time-invariant regressors. This is documented in the manuscript as the primary v2 target.
- **Coverage**: 67 firms (~7% of IDX listings), concentrated among large-cap names.
- **Sharia classification**: Sector-level proxy (10 non-financial sectors flagged compliant). Firm-level OJK DES data planned for v2.
- **No ESG, governance, or macro variables**: Deferred to v2.

---

## Manuscript

The Data Descriptor manuscript is available in this repository:

- [`draft_manuscript.tex`](draft_manuscript.tex) — LaTeX source
- [`draft_manuscript_verified.md`](draft_manuscript_verified.md) — Verified markdown copy

**Target journal**: *Scientific Data* (Nature) → *Data in Brief* (Elsevier) → *BMC Research Notes*

---

## Citation

If you use this dataset or pipeline, please cite:

> Kesuma, A. & Ismail, A. (2026). A Panel Dataset of the Indonesia Stock Exchange: Prices, Fundamentals, and Sharia Classification (2010–2026). *Scientific Data* (under review). Zenodo. https://doi.org/10.5281/zenodo.21110404

### BibTeX

```bibtex
@dataset{kesuma2026panel,
  author       = {Kesuma, Ali and Ismail, Andy},
  title        = {A Panel Dataset of the Indonesia Stock Exchange: Prices, Fundamentals, and Sharia Classification (2010--2026)},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.21110404},
  note         = {Under review at Scientific Data (Nature)}
}
```

---

## License

This work is licensed under **CC-BY 4.0**. You are free to share and adapt for any purpose, provided appropriate credit is given.

---

## Contact

- **Ali Kesuma** — ali@unda.ac.id (corresponding author)
- **Andy Ismail** — andy@unda.ac.id
- Faculty of Business, Universitas Darwan Ali, Indonesia

---

## Links

- [GitHub Repository](https://github.com/lensetek/idx-panel-data-descriptor)
- [Zenodo Record](https://zenodo.org/records/21110404)
- [Codebook](data_acquisition/codebook.md)
