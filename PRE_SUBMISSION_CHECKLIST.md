# Pre-Submission Checklist — IDX Panel Data Descriptor

**Target Journal**: Scientific Data (Nature)
**Deadline**: [TBD]
**Status**: Minor Revision Before Submit

---

## M1: Fix "Comprehensive" Overstatement

**What**: Ganti kata "comprehensive" di title dan body dengan "curated panel of major-cap IDX firms" atau "a panel dataset of IDX non-financial firms."

**Where in draft_manuscript.md**:
- [ ] Title
- [ ] Abstract
- [ ] Background & Summary, paragraph 4
- [ ] Technical Validation section

**Additional**: Hitung market cap coverage. 67 tickers dari 900+ IDX = 7% jumlah. Tapi berapa % total kapitalisasi pasar IDX?

**Command**:
```python
import pandas as pd
fund = pd.read_csv("data_acquisition/raw/idx_fundamentals.csv")
total_mcap = fund["marketCap"].sum()
# Compare to IDX total MCAP ~$600B = ~Rp9,600 triliun
pct = (total_mcap / 9_600_000_000_000_000) * 100  # sesuaikan
print(f"MCAP coverage: {pct:.1f}%")
```

---

## M2: Move FE/GMM Limitation to Technical Validation

**What**: Tambah subsection "Panel Model Limitations" di bawah Technical Validation.

**Content to add**:
> ### Panel Model Limitations
>
> The current v1 release uses cross-sectional financial ratios from a single Yahoo Finance snapshot. As a result, within-firm variation cannot be exploited for fixed-effects estimation — entity effects perfectly absorb the time-invariant regressors. Similarly, Arellano-Bond dynamic panel GMM fails due to perfect collinearity after entity-demeaning. This is not a data defect but a structural limitation of using snapshot fundamentals. We document this as the primary upgrade target for v2 (see Usage Notes).

---

## M3: R² Contextualisation

**What**: Tambah kalimat di Technical Validation Results yang menjelaskan mengapa R²=0.034 wajar.

**Add after regression results**:
> We emphasise that the regression serves as proof-of-concept validation demonstrating that the data structure supports econometric analysis, rather than as a substantive finding. The low R² reflects the dominance of cross-sectional variance in a single-snapshot fundamental dataset, consistent with cross-sectional finance regressions where R² values of 0.02–0.10 are typical.

---

## m1: Shorten Title

**Current**: "A Comprehensive Panel Dataset of the Indonesian Stock Exchange (2010–2026): Stock Prices, Fundamentals, and Sharia Classification"

**Proposed**: "A Panel Dataset of the Indonesia Stock Exchange: Prices, Fundamentals, and Sharia Classification (2010–2026)"

---

## m2: Verify Abstract Word Count

Scientific Data maximum: 250 words.

**Command**:
```python
abstract = """...""
words = len(abstract.split())
print(f"Abstract: {words} words")
```

Fix if >250.

---

## m3: Verify LaTeX Equation Rendering

Scientific Data accepts LaTeX in manuscripts. Equation in Methods section:
```
$$Tobin's Q_i = β_0 + β_1 ROA_i + β_2 DER_i + β_3 Beta_i + ε_i$$
```
Ensure this renders in submission portal.

---

## m4: Verify Sector Classification Source

Change "GICS sector classification" → "Sector classification (source: Yahoo Finance)" unless confirmed GICS.

Check:
```python
import yfinance as yf
t = yf.Ticker("BBRI.JK")
print(t.info.get("sector"))  # Does Yahoo call this GICS?
```

---

## m5: Remove Empty Macro Template

File `idx_macro_template.csv` is nearly empty (NaN placeholders). Either:
- [ ] Remove from published dataset (defer to v2), OR
- [ ] Populate with actual BI Rate, Inflation, GDP data from BI & BPS

**Recommended**: Remove. Mention in Usage Notes as v2 target.

---

## m6: Expand References (10 → 20+)

Scientific Data Data Descriptors typically cite 20-40 references. Add:

| # | Paper | DOI | Purpose |
|---|---|---|---|
| 11 | Additional Scientific Data Data Descriptor (finance/econ) | search SD | Establish precedent |
| 12 | Additional Scientific Data Data Descriptor (social science) | search SD | Broader precedent |
| 13 | Wooldridge "Econometric Analysis of Cross Section and Panel Data" | ISBN | Panel methodology standard |
| 14 | Reference on PBV as Tobin's Q proxy in EM | search | Justify proxy |
| 15 | Additional ESG-Sharia Indonesia study | search | Strengthen RQ3 |
| 16 | OJK DES methodology paper | search | Sharia classification |
| 17 | IDX Annual Statistics | idx.co.id | Market context |
| 18-20 | Additional | — | Fill to 20 |

---

## m7: Add R² to Table 1 Caption

Change:
> **Table 1: Pooled OLS Regression Results (HC3 Robust Standard Errors)**

To:
> **Table 1: Pooled OLS Regression Results (HC3 Robust Standard Errors).** N = 1,107; R² = 0.034; Adjusted R² = 0.032.

---

## Pre-Submission Technical Tasks

- [ ] **Zenodo deposit**: Upload dataset + get provisional DOI
  - Files: `idx_stock_prices.csv`, `idx_fundamentals.csv`, `panel_master.csv`, `idx_ihsg_index.csv`, `idx_tickers_validated.csv`
  - Documentation: `codebook.md`, `README.md`, `LICENSE`
  - DOI placeholder → replace all `[to be assigned]` in manuscript

- [ ] **GitHub repo**: Push scripts + documentation
  - Scripts: `01_get_tickers.py`, `02_get_all_tickers.py`, `03_build_ticker_list.py`, `04_download_data.py`, `05_panel_regression.py`, `06_validation.py`
  - Create public repo: `idx-panel-dataset`
  - Update manuscript GitHub URL

- [ ] **Codebook**: Create `codebook.md` with full variable dictionary

- [ ] **README.md**: Create dataset overview for Zenodo/GitHub

- [ ] **Author info**: Complete author contributions, affiliations, funding, acknowledgements

---

## Submission Order

```
1st → Scientific Data (Nature)  [$2,190 APC]
  ↓ IF REJECTED
2nd → Data in Brief (Elsevier)  [$650 APC]
  ↓ IF REJECTED  
3rd → BMC Research Notes       [$1,120 APC]
```

---

## Quick Python: Market Cap Coverage

```python
import pandas as pd
fund = pd.read_csv("data_acquisition/raw/idx_fundamentals.csv")
fund["marketCap_trillion"] = fund["marketCap"] / 1e12
print(f"Total MCAP: {fund['marketCap'].sum() / 1e12:.1f} trillion IDR")
print(f"Median MCAP: {fund['marketCap'].median() / 1e12:.1f} trillion IDR")
print(f"Top 10 by MCAP:")
print(fund.nlargest(10, "marketCap")[["ticker", "name", "marketCap_trillion"]])
```
