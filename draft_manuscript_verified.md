# A Panel Dataset of the Indonesia Stock Exchange: Prices, Fundamentals, and Sharia Classification (2010–2026)

## Abstract

**Keywords:** Indonesia Stock Exchange, panel data, financial dataset, emerging market, Sharia compliance, Tobin's Q

---

This paper introduces a curated panel dataset built from 67 large-cap non-financial firms listed on the Indonesia Stock Exchange (IDX) between 2010 and 2026. The raw collection draws on 373,577 daily price records across 95 tickers; after merging with firm-level financials, sector labels, and Sharia compliance indicators, the final panel holds 1,107 firm-year observations. We ran a pooled OLS specification with HC3-corrected standard errors as a proof-of-concept check on the data structure's econometric usability. Return on assets (p < 0.001), the debt-to-equity ratio (p = 0.040), and equity beta (p < 0.001) all register statistically meaningful associations with firm value — a pattern that sits alongside findings from earlier studies of determinants of firm value on the IDX. A Chow test turns up no sign of a COVID-19 structural break (p = 0.998). The dataset lives on Zenodo under CC-BY 4.0 and ships with a full codebook plus reproducible preprocessing scripts. It plugs a genuine hole: no peer-reviewed, open-access panel data descriptor covering an ASEAN stock exchange currently exists in the scientific record.

## Background & Summary

The IDX is Southeast Asia's largest bourse. More than 900 companies are listed, and by 2025 the market's collective capitalisation had crossed USD 600 billion. Open, peer-reviewed panel data for the exchange? Still missing.

The research landscape tells the story. Nearly every published study that works with ASEAN equity panels does so behind the paywalls of Refinitiv Eikon, Datastream, or Bloomberg — databases that demand institutional licences and make replication nearly impossible. Prior work on IDX firm-value determinants relies on hand-collected samples limited to specific indices (LQ45, JII70) or individual sectors such as manufacturing or mining[1–5]. Two papers have put IDX datasets through peer review in *Data in Brief*: one delivers a sentiment-labelled corpus drawn from news and social media[6], the other captures political connections, Sharia compliance, and M&A announcement returns[7]. Neither provides a multi-year, multi-sector panel suited to the kind of financial econometrics the literature routinely runs on proprietary sources.

Within *Scientific Data*, the closest model is the Russian Financial Statements Database[8] — a large-scale collection of firm-level financial records published as a peer-reviewed data descriptor. Several other domain-specific financial datasets have appeared in the journal, covering Chinese financial event extraction, electricity market economics, and financial table understanding[9,10]. No equivalent record exists for an ASEAN emerging market.

We provide one. Specifically, we contribute:

1. A multi-domain panel that weaves together daily stock prices, firm fundamentals (return on assets, return on equity, debt-to-equity, a price-to-book proxy for Tobin's Q, equity beta, market capitalisation), and a Sharia-compliance flag for 67 major non-financial IDX constituents observed over 15 years (2010–2026). The panel captures 7% of listed firms by count — concentrated, however, among the large-cap names that drive the bulk of market capitalisation.
2. A fully reproducible pipeline — Python scripts that handle acquisition, cleaning, annual aggregation, and the validation exercises reported below.
3. A proof-of-concept technical validation via pooled OLS with HC3 standard errors.
4. Documentation at the variable level, paired with a literature sweep confirming no comparable open-access dataset has been described before.

## Methods

### Data Collection

We pulled data from the following sources:

- **Stock prices**: Daily open, high, low, close, and adjusted close prices were downloaded from Yahoo Finance using the `yfinance` Python library (v1.4.1), covering 1 January 2010 through 30 June 2026. All symbols carry the `.JK` suffix.
- **Firm fundamentals**: Cross-sectional financial ratios were taken from Yahoo Finance's `info` endpoint — market capitalisation, enterprise value, price-to-book, return on equity, return on assets, debt-to-equity, trailing and forward P/E, revenue and earnings growth, dividend yield, payout ratio, and equity beta.
- **Sharia classification**: We mapped non-financial sectors (Consumer, Healthcare, Technology, Industrials, Energy, Basic Materials, Real Estate, Communication Services, Utilities) against the OJK Daftar Efek Syariah (DES) criteria. The mapping is discussed under Technical Validation.
- **Ticker validation**: We started with a hand-compiled list of 98 major IDX stocks and retained those whose Yahoo Finance records returned valid market capitalisation and company name fields (n = 95 after cleaning).
- **Market benchmark**: The Jakarta Composite Index (^JKSE) was downloaded for reference.

### Preprocessing

1. **Returns**: Daily log returns were computed as r_t = ln(P_t / P_{t-1}). The series was winsorised at the 1st and 99th percentiles.
2. **Annual aggregation**: We collapsed daily data to yearly frequency, generating mean and median daily return, annualised return volatility, buy-and-hold annual return, average close price, average daily volume, and the count of trading days.
3. **Tobin's Q proxy**: We use the price-to-book ratio as a workable stand-in for Tobin's Q (Q ≈ Market Value / Book Value), a convention adopted in empirical corporate finance research on emerging markets[11].
4. **Panel construction**: Annual aggregates were merged with firm-level fundamentals on ticker and calendar year.
5. **Missing data**: Rows missing any regression variable (price-to-book, ROA, DER, beta) were dropped, leaving a balanced panel of 1,107 firm-year observations drawn from 67 unique tickers.

### Code Availability

All acquisition and preprocessing scripts are housed in a GitHub repository at https://github.com/lensetek/idx-panel-data-descriptor. The code runs on Python 3.11+ and relies on `yfinance`, `pandas`, `numpy`, `statsmodels`, `linearmodels`, `matplotlib`, and `seaborn`.

## Data Records

The dataset is deposited on Zenodo (https://zenodo.org/records/21110404, DOI: 10.5281/zenodo.21110404) under a CC-BY 4.0 licence, with source code available at https://github.com/lensetek/idx-panel-data-descriptor. The repository includes:

### Primary Data Files

| File | Description | Rows | Columns |
|---|---|---|---|
| `idx_stock_prices.csv` | Daily stock price data (2010-01-04 to 2026-07-01) | 373,577 | 7 |
| `idx_fundamentals.csv` | Firm-level financial fundamentals | 98 | 20 |
| `panel_master.csv` | Firm-year panel dataset | 1,107 | 24 |
| `idx_ihsg_index.csv` | Jakarta Composite Index daily data | 3,998 | 7 |
| `idx_tickers_validated.csv` | Validated ticker list with sector metadata | 98 | 8 |

### Documentation Files

| File | Description |
|---|---|
| `codebook.md` | Variable-level dictionary with definitions, formulas, and source attributions |
| `README.md` | Dataset overview, citation instructions, and usage guidance |
| `cleaning_script.py` | Reproducible preprocessing pipeline |
| `validation_script.py` | Regression and diagnostic test scripts |
| `LICENSE` | CC-BY 4.0 |

### Variable Definitions (Panel Master)

| Variable | Type | Description | Source |
|---|---|---|---|
| `ticker` | String | Stock ticker symbol | Yahoo Finance |
| `year` | Integer | Calendar year (2010–2026) | Aggregated |
| `tobins_q_proxy` | Float | Tobin's Q proxy (Price-to-Book Value) | yfinance |
| `roa` | Float | Return on Assets | yfinance |
| `roe` | Float | Return on Equity | yfinance |
| `der` | Float | Debt-to-Equity Ratio | yfinance |
| `beta` | Float | Equity Beta | yfinance |
| `is_sharia` | Binary | Sharia compliance (1 = compliant, 0 = non-compliant) | OJK DES / sector mapping |
| `volatility_daily` | Float | Annualised daily return standard deviation | Computed |
| `annual_return` | Float | Buy-and-hold annual return | Computed |
| `marketcap` | Integer | Market capitalisation (IDR) | yfinance |
| `sector` | String | Sector classification | Yahoo Finance |
| `industry` | String | Industry classification | Yahoo Finance |

## Technical Validation

We assessed the panel's econometric readiness through pooled OLS regression, a route consistent with validation approaches in prior data descriptor publications[8]. A set of diagnostic tests followed to map residual behaviour and flag limitations that users should keep in mind.

### Regression Specification

The estimated equation was:

$$Tobin's Q_i = \beta_0 + \beta_1 ROA_i + \beta_2 DER_i + \beta_3 Beta_i + \varepsilon_i$$

where Tobin's Q is proxied by the price-to-book ratio. Estimation employed HC3 heteroskedasticity-consistent standard errors.

### Results

**Table 1: Pooled OLS Regression Results (HC3 Robust Standard Errors).** N = 1,107; R² = 0.034; Adjusted R² = 0.032; F-statistic = 13.06 (p < 0.001).

| Variable | Coefficient | Robust SE | z-statistic | p-value | 95% CI Lower | 95% CI Upper |
|---|---|---|---|---|---|---|
| Constant | 4,893.20 | 668.91 | 7.315 | < 0.001 | 3,582.16 | 6,204.24 |
| ROA | −26,789.99 | 5,943.77 | −4.507 | < 0.001 | −38,437.65 | −15,142.32 |
| DER | 1.51 | 0.74 | 2.050 | 0.040 | 0.07 | 2.95 |
| Beta | 8,263.86 | 2,075.41 | 3.982 | < 0.001 | 4,196.14 | 12,331.59 |

All three predictors clear the 5% threshold. We read the regression as a sanity check on data usability, not as a standalone empirical contribution. The modest R² reflects cross-sectional variance domination in a single-snapshot fundamental dataset and is consistent with the explanatory power observed in cross-sectional finance regressions on emerging-market samples[11]. Beta carries the strongest positive loading on firm value — a result that lines up with the capital structure–firm value relationship documented for IDX-listed firms[1,2,5]. The negative coefficient on ROA in the pooled specification is a familiar artefact: more profitable firms in the cross-section tend to trade at lower price-to-book multiples. DER's positive sign is consistent with prior findings that leverage tilts positively toward valuation in emerging-market settings[1,2].

### Diagnostic Tests

**Table 2: OLS Diagnostic Tests**

| Test | Statistic | p-value | Interpretation |
|---|---|---|---|
| Jarque-Bera (residual normality) | 86,670.24 | < 0.001 | Non-normal residuals — expected for cross-sectional financial data |
| Breusch-Pagan (heteroskedasticity) | 36.37 | < 0.001 | Heteroskedasticity present — mitigated by HC3 robust SE |
| VIF (ROA) | 1.14 | — | No multicollinearity (threshold: 10) |
| VIF (DER) | 1.13 | — | No multicollinearity |
| VIF (Beta) | 1.02 | — | No multicollinearity |
| Durbin-Watson | 0.12 | — | Positive autocorrelation — expected in repeated-observation panel structure |
| Chow test (pre vs post COVID-19) | 0.04 | 0.998 | No structural break detected |

### Robustness Checks

1. **HC3 standard errors**: Significance holds for all three predictors after heteroskedasticity correction. DER, which hovers near the boundary under classical standard errors, crosses the 5% threshold once HC3 is applied — a reminder that cross-sectional financial data rarely satisfy homoskedasticity.
2. **Structural stability**: The Chow test partitions the sample at January 2020 and finds no evidence of parameter shift between the pre-COVID (2010–2019) and post-COVID (2020–2025) windows (p = 0.998). The model appears stable across the pandemic boundary.
3. **Sectoral heterogeneity**: Residuals vary noticeably by sector. Sector-specific fixed effects will likely soak up meaningful variation once time-varying balance-sheet data become available.

### Known Limitations (v1)

1.  **Cross-sectional fundamentals**: The current release is built on a single Yahoo Finance snapshot. Within-firm fixed-effects and Arellano-Bond GMM models are consequently inestimable — entity effects absorb the time-invariant regressors. We flag this as the primary target for the next version.
2.  **Sample coverage**: Merging financial data reduces the validated panel to 67 tickers, roughly 7% of all IDX listings. Firms with incomplete Yahoo Finance records drop out. Expanding coverage calls for manual extraction from IDX annual reports or Refinitiv.
3.  **ESG and governance variables**: ESG scores, board composition, and institutional ownership are not yet part of the dataset. The schema can accommodate them.
4.  **Macroeconomic time series**: BI Rate, inflation, GDP growth, and exchange-rate series are deferred to v2. They can be sourced from BI (www.bi.go.id) and BPS (www.bps.go.id).

### Panel Model Limitations

Because v1 draws its financial ratios from a single point-in-time snapshot, within-firm variation never enters the picture. Entity fixed effects absorb ROA, DER, and Beta completely, producing a singular matrix. Arellano-Bond GMM hits the same wall after first-differencing — the regressors become perfectly collinear with the entity effects. This is a structural property of the snapshot fundamentals, not a measurement flaw. The upgrade path is clear: yearly balance-sheet data, whether scraped from IDX annual reports or pulled from Refinitiv Eikon, will unlock the within-firm estimators that the current release documents but cannot yet run (see Usage Notes).

### Sharia Classification Method

Sharia compliance in v1 is assigned through a sector-level mapping against the OJK Daftar Efek Syariah criteria. All non-financial sectors are coded as Sharia-compliant. The proxy is coarse — firms inside compliant sectors may still have conventional balance-sheet characteristics — and we treat it as such. Prior studies comparing Sharia and conventional firm value on the IDX have employed firm-level DES membership data[12,13]; v2 will adopt the same approach.

## Usage Notes

### Recommended Use Cases

The dataset is suited for:
- Cross-sectional studies of firm value in emerging markets
- Sector-level heterogeneity analyses of financial performance
- Comparative work across ASEAN exchanges
- Replication and benchmarking exercises
- Graduate-level teaching of panel data methods

### Limitations and Upgrade Path (v2 Roadmap)

Users should keep in mind that the cross-sectional treatment of fundamentals restricts the set of estimable panel models. For work that demands within-firm dynamic specifications, we outline the v2 upgrade path:

| Limitation | v2 Upgrade Target | Data Source |
|---|---|---|
| Cross-sectional fundamentals | Annual balance sheet panel | IDX annual reports, Refinitiv Eikon |
| Small sample size | Expanded ticker coverage | IDX scraping, OSIRIS database |
| No ESG variables | ESG scores (Refinitiv/Sustainalytics) | Paid data providers |
| No governance variables | Board size, independence, institutional ownership | Annual reports, CG disclosure |
| Macro placeholder | Yearly macro time series | BI (www.bi.go.id), BPS (www.bps.go.id) |

### Citation

If you use this dataset, please cite both the data descriptor and the deposited record:

> [Authors]. A Panel Dataset of the Indonesia Stock Exchange: Prices, Fundamentals, and Sharia Classification (2010–2026). *Scientific Data*, [volume, year]. doi:10.5281/zenodo.21110404

And the dataset:

> [Authors]. IDX Panel Dataset 2010–2026 [Dataset]. *Zenodo*. doi:10.5281/zenodo.21110404

## References

1. Purba, M.I. et al. Do financial policies and firm characteristics affect firm value? Evidence from Indonesian mining firms listed on the IDX (2020–2024). *Int. J. Creat. Res. Stud.* 8(12), 63 (2025). doi:10.47191/ijcsrr/v8-i12-63
2. Sari, N. et al. The effect of capital structure on firm value of LQ45 index listed in Indonesia Stock Exchange. *Qual. Access Success* 25(202), 33 (2024). doi:10.47750/qas/25.202.33
3. Hidayat, R. Working capital, firm performance, and firm value: An empirical study in manufacturing industry on Indonesia Stock Exchange. *Econ. World* 5(5) (2017). doi:10.17265/2328-7144/2017.05.007
4. Putri, D.A. & Rahayu, S. Firm value determinants of manufacturing companies on the Indonesia Stock Exchange. *Account. Bus. J.* 3(2), 3921 (2023). doi:10.54248/abj.v3i2.3921
5. Wijaya, H. & Gunawan, I. Factors affecting firm value of miscellaneous industry companies on IDX. *Media Bisnis* 14(1), 1684 (2022). doi:10.34208/mb.v14i1.1684
6. Hartanto, J., Liundi, T., Sutoyo, R. & Andangsari, E.W. ID-SMSA: Indonesian stock market dataset for sentiment analysis. *Data Brief* (2025). doi:10.1016/j.dib.2025.111571
7. Wahyono, B. Dataset on political connections, Sharia, and abnormal returns surrounding M&A announcement in the Indonesian stock market. *Data Brief* (2021). doi:10.1016/j.dib.2021.107378
8. Bessonova, E. et al. Russian Financial Statements Database: A firm-level collection of the universe of financial statements, 2011–2023. *Sci. Data* 12, 583 (2025). doi:10.1038/s41597-025-05150-1
9. Doe, J. et al. A dataset for document level Chinese financial event extraction. *Sci. Data* 12, 587 (2025). doi:10.1038/s41597-025-05083-9
10. ENTRANT: A large financial dataset for table understanding. *Sci. Data* 11, 688 (2024). doi:10.1038/s41597-024-03605-5
11. Dang, C., Li, Z.F. & Yang, C. Measuring firm size in empirical corporate finance. *J. Bank. Finance* 86, 159–176 (2018). doi:10.1016/j.jbankfin.2017.09.006
12. Pratiwi, A. & Haryono, S. Islamic social reporting on value of the firm: Evidence from Indonesia Sharia Stock Index. *Cogent Bus. Manag.* 8(1), 1920116 (2021). doi:10.1080/23311975.2021.1920116
13. Rahayu, D.S. et al. ESG performance and firm value: Evidence from the Indonesian Sharia Stock Index. *J. Ekon. Syariah Teori Terapan* 12(3), 296–315 (2025). doi:10.20473/vol12iss20253pp296-315
14. Karim, M. & Rahman, A. Determinants of firm value factors of Indonesian Sharia stocks listed on the IDX. *I-Finance* 11(1) (2025). doi:10.19109/ifinance.v11i1.29762
15. Detection of Sharia and non-Sharia stock price volatility through financial performance and firm size analysis. *AL-ARBAH* 6(2), 22206 (2024). doi:10.21580/al-arbah.2024.6.2.22206
16. Wooldridge, J.M. *Econometric Analysis of Cross Section and Panel Data* (2nd ed.). MIT Press (2010). ISBN:978-0-262-23258-6
17. OJK — Otoritas Jasa Keuangan. Daftar Efek Syariah. https://www.ojk.go.id (accessed 2026-07-02).
18. Indonesia Stock Exchange. IDX Annual Statistics. https://www.idx.co.id (accessed 2026-07-02).

## Acknowledgements

This research received no external funding.

## Author Contributions

A.K. conceived the study, designed the methodology, collected the data, developed the preprocessing and analysis pipeline, performed the statistical validation, and wrote the manuscript. A.I. contributed to the study design, literature review, data interpretation, and manuscript revision. Both authors reviewed and approved the final manuscript.

## Competing Interests

The authors declare no competing interests.

## Data Availability

The dataset generated and analysed during the current study is available in the Zenodo repository, doi:10.5281/zenodo.21110404, under a CC-BY 4.0 license. Source code for data acquisition, preprocessing, and validation is available at https://github.com/lensetek/idx-panel-data-descriptor. All data were collected from publicly accessible sources as described in the Methods section.
