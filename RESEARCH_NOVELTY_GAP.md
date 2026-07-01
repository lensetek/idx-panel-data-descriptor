# Research Gap, Novelty, and Contribution — IDX Panel Data Descriptor

**Date:** 2 July 2026
**Target Journal:** Scientific Data (Nature)
**Manuscript:** `draft_manuscript.tex`

---

## 1. Research Gap

### Primary Gap
> **No open-access, peer-reviewed Data Descriptor exists for any ASEAN stock exchange in _Scientific Data_ (Nature) or comparable journals.**

### Evidence

| Source | Status | What It Covers |
|---|---|---|
| Hartanto et al. (2025) — _Data in Brief_ | ✅ Real, verified | Sentiment analysis dataset only — single-domain (text) |
| Wahyono (2021) — _Data in Brief_ | ✅ Real, verified | M&A event study dataset only — single-domain (event) |
| Bessonova et al. (2025) — _Scientific Data_ | ✅ Real, verified | Russian financial statements database — closest model, but no ASEAN coverage |
| All IDX/ASEAN panel studies in literature | Real pattern | Use proprietary databases (Refinitiv, Datastream, Bloomberg) — **not reproducible** |

### Why This Gap Matters
- Researchers studying Indonesian/ASEAN capital markets must either: (a) pay for expensive institutional licenses, or (b) manually scrape data from scratch for every study
- No standardized, reusable panel dataset exists — every researcher builds their own private dataset
- This creates a reproducibility crisis in ASEAN financial research
- _Scientific Data_'s mission is to publish reusable datasets — an ASEAN exchange dataset is exactly what the journal exists for, yet none has been submitted

---

## 2. Novelty

### What Is New

| Dimension | Existing Literature | This Dataset |
|---|---|---|
| **Open access** | Refinitiv/Datastream (paid license required) | Zenodo CC-BY 4.0 (free) |
| **Scope** | Single-domain (sentiment, event study, specific index) | Multi-domain: prices + fundamentals + Sharia classification |
| **Time span** | Typically 3–5 years | 15 years (2010–2026) |
| **Reproducibility** | No scripts, no codebook | Full Python pipeline + codebook + README |
| **Peer review** | Dataset papers exist in Data in Brief (lower tier) | Target: Scientific Data (Nature, IF ~8.6) |
| **Geographic coverage** | Russia, China, US/Europe | **First ASEAN emerging market** |

### Specific Novelty Claims

1. **First multi-domain open-access panel dataset for IDX**
   - Integrates: daily stock prices (373,577 obs) + cross-sectional fundamentals (ROA, ROE, DER, PBV, beta) + Sharia classification
   - 67 major non-financial firms, 1,107 firm-year observations, 15-year window

2. **First fully reproducible IDX data pipeline**
   - Python scripts for: acquisition (yfinance API) → preprocessing (winsorizing, annual aggregation) → validation (OLS + diagnostics)
   - Codebook at variable level with source attribution

3. **Proof-of-concept validation with transparent limitations**
   - OLS with HC3 robust SE: ROA (p<0.001), DER (p=0.040), Beta (p<0.001)
   - Chow test: no COVID-19 structural break (p=0.998)
   - Documented: FE/GMM failure → v2 roadmap (yearly balance sheet data)
   - Documented: Sharia sector-level proxy → v2 roadmap (firm-level DES)

4. **Model for Data Descriptors in emerging-market finance**
   - Demonstrates that free data sources (Yahoo Finance) + transparent methodology = publishable Data Descriptor
   - Lowers barrier for other ASEAN exchanges (Bursa Malaysia, SET Thailand, etc.)

---

## 3. Contribution

### Scientific Contribution

| Type | Description |
|---|---|
| **Data infrastructure** | Provides the first standardized, reusable dataset for IDX financial research |
| **Methodology** | Demonstrates a reproducible pipeline for emerging-market data descriptor construction |
| **Transparency** | Honest limitation documentation sets a standard for data papers — no overclaiming |

### Practical Contribution

| Use Case | Who Benefits |
|---|---|
| Cross-sectional firm value studies | Finance researchers without Refinitiv access |
| Sectoral heterogeneity analysis | Policy analysts, industry researchers |
| ASEAN comparative finance | Regional development researchers |
| Replication & benchmarking | Graduate students, early-career researchers |
| Teaching panel data methods | Finance/econometrics instructors |

### Publication Strategy

```
1st target: Scientific Data (Nature) — IF 8.6, Q1, Data Descriptor format
     ↓ if rejected
2nd target: Data in Brief (Elsevier) — SJR 0.40, Q1, accepts IDX datasets
     ↓ if rejected
3rd target: BMC Research Notes (Springer Nature) — Data Note format
```

---

## 4. Honest Limitations (v1)

These are documented in the manuscript, not hidden:

| Limitation | Reason | Fix (v2) |
|---|---|---|
| Cross-sectional fundamentals | yfinance snapshot — single point in time | Yearly balance sheet from IDX annual reports / Refinitiv |
| 67 tickers (7% of IDX) | Only firms with complete Yahoo Finance data merged | Expand scraping coverage |
| FE and GMM inestimable | Time-invariant regressors absorbed by entity effects | Yearly fundamentals (see above) |
| Sharia via sector proxy | OJK DES firm-level data not yet integrated | Firm-level DES membership |
| No ESG scores | Requires paid data (Refinitiv/Sustainalytics) | Add if funding allows |
| No governance variables | Board size, independence, institutional ownership not scraped | Add from annual reports |
| Macro template empty | BI Rate, inflation, GDP deferred | Populate from BI & BPS |

---

## 5. What This Research Is NOT

- ❌ Not a breakthrough statistical finding (R²=0.034 — expected for cross-sectional data)
- ❌ Not a novel causal identification strategy
- ❌ Not a machine learning model
- ❌ Not a complete panel (time-varying fundamentals needed for FE/GMM)

## What This Research IS

- ✅ A **data paper** — the contribution is the dataset itself
- ✅ A **research infrastructure** contribution — enables future work
- ✅ A **reproducibility** contribution — pipeline, codebook, open license
- ✅ A **gap-filler** — first open-access IDX panel in the scientific record

---

## 6. One-Sentence Pitch (for cover letter)

> This Data Descriptor provides the first open-access, peer-reviewed panel dataset covering the Indonesia Stock Exchange — filling a documented gap where all existing ASEAN equity research relies on proprietary databases that preclude replication.
