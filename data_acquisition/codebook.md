# Codebook — IDX Panel Dataset (2010–2026)

## Dataset Overview

- **Repository**: https://github.com/lensetek/idx-panel-data-descriptor
- **License**: CC-BY 4.0
- **Citation**: Kesuma, A. & Ismail, A. A Panel Dataset of the Indonesia Stock Exchange: Prices, Fundamentals, and Sharia Classification (2010–2026). *Scientific Data* (under review). Zenodo. doi:[to be assigned]

---

## File: `idx_stock_prices.csv`

Daily stock price data downloaded from Yahoo Finance via `yfinance` v1.4.1.

| Variable | Type | Description |
|---|---|---|
| `ticker` | string | Stock ticker symbol (Yahoo Finance `.JK` suffix removed) |
| `date` | date | Trading date (YYYY-MM-DD) |
| `open` | float | Opening price (IDR) |
| `high` | float | Highest price of the day (IDR) |
| `low` | float | Lowest price of the day (IDR) |
| `close` | float | Closing price (IDR), adjusted for splits and dividends |
| `volume` | float | Number of shares traded |

- **Rows**: 373,577
- **Tickers**: 95
- **Period**: 2010-01-04 to 2026-07-01
- **Missing values**: None (only tickers with complete price history retained)

---

## File: `idx_fundamentals.csv`

Firm-level financial fundamentals extracted from Yahoo Finance `info` endpoint. Snapshot as of download date (July 2026).

| Variable | Type | Description |
|---|---|---|
| `ticker` | string | Stock ticker symbol |
| `name` | string | Company name |
| `sector` | string | GICS-equivalent sector classification |
| `industry` | string | Industry classification |
| `marketcap` | integer | Market capitalisation (IDR) |
| `enterpriseValue` | float | Enterprise value (marketcap + net debt, IDR) |
| `trailingPE` | float | Trailing price-to-earnings ratio (may be NaN) |
| `forwardPE` | float | Forward price-to-earnings ratio (may be NaN) |
| `priceToBook` | float | Price-to-book ratio |
| `returnOnEquity` | float | Return on equity |
| `returnOnAssets` | float | Return on assets |
| `debtToEquity` | float | Debt-to-equity ratio (%) |
| `revenueGrowth` | float | Revenue growth (YoY) |
| `earningsGrowth` | float | Earnings growth (YoY, may be NaN) |
| `dividendYield` | float | Dividend yield (may be NaN) |
| `payoutRatio` | float | Payout ratio (may be NaN) |
| `beta` | float | Equity beta (5-year monthly) |
| `fiftyTwoWeekHigh` | float | 52-week high price (IDR) |
| `fiftyTwoWeekLow` | float | 52-week low price (IDR) |
| `currency` | string | Currency (all IDR) |

- **Rows**: 98
- **Note**: Values are cross-sectional (single snapshot), not time-varying. See manuscript Limitations for implications.

---

## File: `panel_master.csv`

Firm-year panel dataset. Primary file for econometric analysis.

| Variable | Type | Description | Source |
|---|---|---|---|
| `ticker` | string | Stock ticker symbol | Yahoo Finance |
| `year` | integer | Calendar year (2010–2026) | Aggregated from daily data |
| `mean_return_daily` | float | Mean daily log return | Computed (winsorised 1%/99%) |
| `median_return_daily` | float | Median daily log return | Computed |
| `volatility_daily` | float | Standard deviation of daily log returns | Computed (annualised) |
| `annual_return` | float | Buy-and-hold annual return | Computed: `close[-1] / close[0] - 1` |
| `mean_close` | float | Average closing price (IDR) | Computed |
| `mean_volume` | float | Average daily trading volume | Computed |
| `total_volume` | float | Total shares traded in the year | Computed |
| `trading_days` | integer | Number of trading days in the year | Count |
| `sector` | string | Sector classification | Yahoo Finance |
| `industry` | string | Industry classification | Yahoo Finance |
| `marketcap` | integer | Market capitalisation (IDR) | yfinance snapshot |
| `ev` | float | Enterprise value (IDR) | yfinance snapshot |
| `tobins_q_proxy` | float | Tobin's Q proxy = Price-to-Book ratio | yfinance |
| `roe` | float | Return on Equity | yfinance snapshot |
| `roa` | float | Return on Assets | yfinance snapshot |
| `der` | float | Debt-to-Equity ratio | yfinance snapshot |
| `revenueGrowth` | float | Revenue growth (YoY) | yfinance snapshot |
| `earningsGrowth` | float | Earnings growth (YoY, may be NaN) | yfinance snapshot |
| `beta` | float | Equity beta | yfinance snapshot |
| `is_financial` | boolean | Financial sector flag | Derived |
| `is_sharia` | integer | Sharia compliance (1 = yes, 0 = no) | OJK DES / sector mapping |

- **Rows**: 1,107
- **Tickers**: 67
- **Years**: 2010–2026
- ⚠️ **Important**: `tobins_q_proxy`, `roa`, `roe`, `der`, `beta`, `marketcap`, `ev`, `revenueGrowth`, and `earningsGrowth` are **cross-sectional** (constant per ticker across all years). This limits panel model estimation. See `validation_report.md` for details.

### Sharia Classification

Sharia compliance (`is_sharia`) is assigned via sector-level mapping:
- **Compliant (1)**: Basic Materials, Communication Services, Consumer Cyclical, Consumer Defensive, Energy, Healthcare, Industrials, Real Estate, Technology, Utilities
- **Not compliant (0)**: Financial Services

This is a coarse proxy. v2 will use firm-level DES membership from OJK. See manuscript for discussion.

---

## File: `idx_ihsg_index.csv`

Jakarta Composite Index (IHSG) daily data.

| Variable | Type | Description |
|---|---|---|
| `date` | date | Trading date |
| `open`, `high`, `low`, `close` | float | Index values |
| `volume` | float | Market volume |

- **Rows**: 3,998
- **Period**: 2010-01-04 to 2026-07-01

---

## File: `idx_tickers_validated.csv`

Master ticker list with validation status.

| Variable | Type | Description |
|---|---|---|
| `ticker` | string | Stock ticker (Yahoo Finance `.JK` suffix removed) |
| `yahoo_ticker` | string | Full Yahoo Finance symbol (`TICKER.JK`) |
| `name` | string | Company name |
| `sector` | string | Sector classification |
| `industry` | string | Industry classification |
| `marketCap` | integer | Market capitalisation (IDR) |
| `currency` | string | Currency |

- **Rows**: 98

---

## Preprocessing Pipeline

All preprocessing steps are reproducible via scripts in the GitHub repository:
1. `04_download_data.py` — Downloads raw price and fundamental data
2. `05_panel_regression.py` — Computes returns, annual aggregation, merges fundamentals, runs OLS
3. `06_validation.py` — Diagnostic tests, Chow test, robust SE

Key processing decisions:
- Log returns winsorised at 1st and 99th percentiles
- Price-to-book used as Tobin's Q proxy
- Observations with missing ROA, DER, or beta excluded
- Only non-financial firms retained for the panel master

---

## Licensing

This dataset is licensed under the **Creative Commons Attribution 4.0 International (CC-BY 4.0)** license.
You are free to share and adapt the data, provided you give appropriate credit.

## Contact

- **Ali Kesuma** (corresponding) — ali@unda.ac.id
- **Andy Ismail** — andy@unda.ac.id
- Faculty of Business, Universitas Darwan Ali, Indonesia
