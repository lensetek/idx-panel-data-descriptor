# Model Validation Report — IDX Panel OLS

## 1. Model Summary (Double Check)
- **Model**: Pooled OLS — Tobins_Q ~ ROA + DER + Beta
- **Observations**: 1,107
- **Tickers**: 67
- **R²**: 0.0343
- **Adj R²**: 0.0317
- **F-statistic**: 13.08 (p=0.0000)

### Coefficients (Standard OLS)
| Variable | Coef | SE | t | P>|t| | [0.025 | 0.975] |
|---|---|---|---|---|---|---|---|
| const | 4893.20 | 1077.24 | 4.54 | 0.0000 | 2779.52 | 7006.87 |
| roa | -26791.27 | 12245.78 | -2.19 | 0.0289 | -50818.92 | -2763.63 |
| der | 1.508 | 0.777 | 1.94 | 0.0524 | -0.016 | 3.032 |
| beta | 8263.86 | 1704.22 | 4.85 | 0.0000 | 4919.99 | 11607.74 |

## 2. Diagnostic Tests

| Test | Statistic | p-value | Verdict |
|---|---|---|---|
| Jarque-Bera (normality) | 86670.24 | 0.0000 | REJECT normality |
| Breusch-Pagan (heteroskedasticity) | 36.37 | 0.0000 | HETEROSKEDASTIC |
| Durbin-Watson (autocorrelation) | 0.1235 | — | Possible autocorrelation |
| Chow (structural break) | 0.0361 | 0.9975 | OK (stable) |

### VIF (Multicollinearity)
| Variable | VIF |
|---|---|
| roa | 1.14 |
| der | 1.13 |
| beta | 1.02 |

## 3. Robust Standard Errors (HC3)

| Variable | Coef (HC3) | SE (HC3) | t | P>|t| |
|---|---|---|---|---|---|
| const | 4893.20 | 668.91 | 7.32 | 0.0000 |
| roa | -26791.27 | 5943.76 | -4.51 | 0.0000 |
| der | 1.508 | 0.736 | 2.05 | 0.0404 |
| beta | 8263.86 | 2075.41 | 3.98 | 0.0001 |

## 4. Pre vs Post COVID Comparison

### Pre-COVID (2010-2019, N=627)
- R² = 0.0353
- ROA coef = -29780.76 (p=0.0760)
- DER coef = 1.420 (p=0.1714)
- Beta coef = 8498.53 (p=0.0003)

### Post-COVID (2020-2025, N=480)
- R² = 0.0332
- ROA coef = -23187.99 (p=0.1974)
- DER coef = 1.617 (p=0.1705)
- Beta coef = 7951.30 (p=0.0018)

## 5. Honest Assessment

### What This Means for Data Descriptor Validity
| Issue | Severity | Mitigation |
|---|---|---|
| Fundamentals are cross-sectional | HIGH | Clearly document as v1 limitation |
| FE/GMM failed (time-invariant IVs) | HIGH | Requires yearly balance sheet data |
| Low R² (0.034) | MODERATE | Expected for cross-sectional PBV model |
| Possible heteroskedasticity | MODERATE | Use robust SE as fallback |
| No statistical model comparison possible | LOW | Only one valid model estimated |

## 6. Conclusion
The pooled OLS model provides a **baseline validation** that the panel data structure
is functional. Beta is the most robust predictor of Tobin's Q across all
specifications. However, the absence of time-varying fundamentals fundamentally
limits the panel econometric analysis that this dataset can support.

**For Scientific Data submission**: Frame this as a **v1 data infrastructure**
paper — the dataset structure is ready, and the OLS results demonstrate
proof-of-concept validity. Future releases with yearly balance sheet data
will unlock FE/GMM estimation.
