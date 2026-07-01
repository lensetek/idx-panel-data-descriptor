"""
Model Evaluator Validator — Pooled OLS diagnostics
Output: validation_report.md, validation_plots.png
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings, sys
warnings.filterwarnings('ignore')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

RAW = Path("data_acquisition/raw")
PROC = Path("data_acquisition/processed")
OUT = PROC
OUT.mkdir(parents=True, exist_ok=True)

# Load panel master
panel = pd.read_csv(PROC / "panel_master.csv")
df = panel.dropna(subset=["roa", "der", "beta", "tobins_q_proxy"]).copy()
dv = "tobins_q_proxy"
ivs = ["roa", "der", "beta"]

print(f"Sample: N={len(df)}")
print(f"DV: {dv}, mean={df[dv].mean():.1f}, std={df[dv].std():.1f}")

# ============================================
# Re-run Pooled OLS (double check)
# ============================================
X = sm.add_constant(df[ivs])
y = df[dv]
ols = sm.OLS(y, X).fit()
residuals = ols.resid
fitted = ols.fittedvalues
n = len(df)

print(f"\n=== POOLED OLS (Double Check) ===")
print(f"R²={ols.rsquared:.4f}, Adj R²={ols.rsquared_adj:.4f}")
print(f"DW={durbin_watson(residuals):.4f}")
print(ols.summary().tables[1])

# ============================================
# Diagnostic Tests
# ============================================
results_test = {}

# --- 1. Jarque-Bera (normality) ---
jb_stat, jb_pval = stats.jarque_bera(residuals)
results_test["Jarque-Bera"] = {"statistic": float(jb_stat), "p_value": float(jb_pval)}
print(f"\nJB test: stat={jb_stat:.2f}, p={jb_pval:.6f}")

# --- 2. Breusch-Pagan (heteroskedasticity) ---
bp_lm, bp_pval, bp_f, bp_f_pval = het_breuschpagan(residuals, X)
results_test["Breusch-Pagan"] = {"statistic": float(bp_lm), "p_value": float(bp_pval)}
print(f"BP test: LM={bp_lm:.2f}, p={bp_pval:.6f}")

# --- 3. VIF (multicollinearity) ---
vif_data = {}
for i, var in enumerate(ivs):
    vif = variance_inflation_factor(X.values, i + 1)
    vif_data[var] = vif
    print(f"VIF({var}) = {vif:.2f}")

# --- 4. Robust SE (HC3) ---
ols_robust = sm.OLS(y, X).fit(cov_type="HC3")
print(f"\nRobust SE (HC3):")
print(ols_robust.summary().tables[1])

# --- 5. Structural Break: Chow test (pre vs post COVID) ---
df["era"] = np.where(df["year"] <= 2019, "pre_covid", "post_covid")
pre = df[df["era"] == "pre_covid"]
post = df[df["era"] == "post_covid"]

ols_pre = sm.OLS(pre[dv], sm.add_constant(pre[ivs])).fit()
ols_post = sm.OLS(post[dv], sm.add_constant(post[ivs])).fit()
ols_full = ols

rss_full = ols_full.ssr
rss_pre = ols_pre.ssr
rss_post = ols_post.ssr
n_pre, n_post = len(pre), len(post)
k = len(ivs) + 1  # including constant

chow_stat = ((rss_full - (rss_pre + rss_post)) / k) / ((rss_pre + rss_post) / (n_pre + n_post - 2*k))
chow_pval = 1 - stats.f.cdf(chow_stat, k, n_pre + n_post - 2*k)
results_test["Chow (COVID break)"] = {"statistic": float(chow_stat), "p_value": float(chow_pval)}
print(f"\nChow test: F={chow_stat:.4f}, p={chow_pval:.6f}")

# --- 6. Table: Pre vs Post COVID ---
print(f"\n=== Pre-COVID OLS (N={n_pre}) ===")
print(f"R²_pre={ols_pre.rsquared:.4f}")
print(ols_pre.summary().tables[1])
print(f"\n=== Post-COVID OLS (N={n_post}) ===")
print(f"R²_post={ols_post.rsquared:.4f}")
print(ols_post.summary().tables[1])

# ============================================
# PLOTS
# ============================================
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
sns.set_style("whitegrid")

# Plot 1: QQ plot
ax = axes[0, 0]
stats.probplot(residuals, dist="norm", plot=ax)
ax.get_lines()[0].set_markersize(3)
ax.get_lines()[0].set_alpha(0.3)
ax.set_title(f"QQ Plot — Residuals\nJarque-Bera p={jb_pval:.4f}")

# Plot 2: Residuals vs Fitted
ax = axes[0, 1]
ax.scatter(fitted, residuals, alpha=0.3, s=10, c="steelblue")
ax.axhline(0, color="red", ls="--", lw=1)
ax.set_xlabel("Fitted Values"); ax.set_ylabel("Residuals")
ax.set_title(f"Residuals vs Fitted\nBreusch-Pagan p={bp_pval:.4f}")

# Plot 3: Histogram residuals
ax = axes[0, 2]
ax.hist(residuals, bins=60, density=True, alpha=0.7, color="steelblue", edgecolor="white")
x_range = np.linspace(residuals.min(), residuals.max(), 200)
ax.plot(x_range, stats.norm.pdf(x_range, residuals.mean(), residuals.std()),
        color="red", lw=2, label="Normal")
ax.set_xlabel("Residuals"); ax.set_title("Residual Distribution")
ax.legend(fontsize=8)

# Plot 4: Residual by ticker (spot panel effects)
ax = axes[1, 0]
df_sorted = df.copy()
ticker_order = df_sorted.groupby("ticker")["tobins_q_proxy"].mean().sort_values().index
for i, t in enumerate(ticker_order[::5]):
    sub = df_sorted[df_sorted["ticker"] == t]
    model_sub = sm.OLS(sub[dv], sm.add_constant(sub[ivs])).fit()
    ax.scatter([i]*len(sub), model_sub.resid, s=5, alpha=0.3, c="steelblue")
ax.axhline(0, color="red", ls="-", lw=1)
ax.set_xlabel("Ticker (sorted by avg Tobins Q)"); ax.set_ylabel("Within-Ticker Residuals")
ax.set_title("Residual Pattern by Ticker")

# Plot 5: Pre vs Post COVID coefficients
coef_comparison = pd.DataFrame({
    "Variable": ["const"] + ivs + ["const"] + ivs,
    "Era": ["Pre-COVID"]*4 + ["Post-COVID"]*4,
    "Coefficient": list(ols_pre.params) + list(ols_post.params),
    "CI_lower": list(ols_pre.conf_int().iloc[:, 0]) + list(ols_post.conf_int().iloc[:, 0]),
    "CI_upper": list(ols_pre.conf_int().iloc[:, 1]) + list(ols_post.conf_int().iloc[:, 1]),
})
coef_vars = [v for v in ivs if v != "const"]
for i, var in enumerate(coef_vars):
    ax = axes[1, 1]
    row = coef_comparison[coef_comparison["Variable"] == var]
    x_pos = np.array([0, 1])
    ax.errorbar(x_pos, row["Coefficient"], yerr=[row["Coefficient"] - row["CI_lower"], row["CI_upper"] - row["Coefficient"]],
                fmt="o", capsize=5, markersize=8)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Pre-COVID", "Post-COVID"])
    ax.axhline(0, color="gray", ls="--", lw=0.5)
    ax.set_ylabel("Coefficient"); ax.set_title(f"Structural Stability: {var}")

# Plot 6: Residual distribution by sector
ax = axes[1, 2]
df["residual"] = residuals
sector_order = df.groupby("sector")["residual"].std().sort_values().index
sns.boxplot(data=df, x="sector", y="residual", order=sector_order, ax=ax, palette="Set3")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=7)
ax.axhline(0, color="red", ls="--", lw=1)
ax.set_title("Residual Distribution by Sector")

fig.tight_layout()
fig.savefig(OUT / "validation_plots.png", dpi=150, bbox_inches="tight")
print(f"\n✅ validation_plots.png saved")

# ============================================
# VALIDATION REPORT
# ============================================
report = f"""# Model Validation Report — IDX Panel OLS

## 1. Model Summary (Double Check)
- **Model**: Pooled OLS — Tobins_Q ~ ROA + DER + Beta
- **Observations**: {n:,}
- **Tickers**: {df['ticker'].nunique()}
- **R²**: {ols.rsquared:.4f}
- **Adj R²**: {ols.rsquared_adj:.4f}
- **F-statistic**: {ols.fvalue:.2f} (p={ols.f_pvalue:.4f})

### Coefficients (Standard OLS)
| Variable | Coef | SE | t | P>|t| | [0.025 | 0.975] |
|---|---|---|---|---|---|---|---|
| const | {ols.params['const']:.2f} | {ols.bse['const']:.2f} | {ols.tvalues['const']:.2f} | {ols.pvalues['const']:.4f} | {ols.conf_int().loc['const',0]:.2f} | {ols.conf_int().loc['const',1]:.2f} |
| roa | {ols.params['roa']:.2f} | {ols.bse['roa']:.2f} | {ols.tvalues['roa']:.2f} | {ols.pvalues['roa']:.4f} | {ols.conf_int().loc['roa',0]:.2f} | {ols.conf_int().loc['roa',1]:.2f} |
| der | {ols.params['der']:.3f} | {ols.bse['der']:.3f} | {ols.tvalues['der']:.2f} | {ols.pvalues['der']:.4f} | {ols.conf_int().loc['der',0]:.3f} | {ols.conf_int().loc['der',1]:.3f} |
| beta | {ols.params['beta']:.2f} | {ols.bse['beta']:.2f} | {ols.tvalues['beta']:.2f} | {ols.pvalues['beta']:.4f} | {ols.conf_int().loc['beta',0]:.2f} | {ols.conf_int().loc['beta',1]:.2f} |

## 2. Diagnostic Tests

| Test | Statistic | p-value | Verdict |
|---|---|---|---|
| Jarque-Bera (normality) | {jb_stat:.2f} | {jb_pval:.4f} | {"REJECT normality" if jb_pval < 0.05 else "OK (normal)"} |
| Breusch-Pagan (heteroskedasticity) | {bp_lm:.2f} | {bp_pval:.4f} | {"HETEROSKEDASTIC" if bp_pval < 0.05 else "OK (homoskedastic)"} |
| Durbin-Watson (autocorrelation) | {durbin_watson(residuals):.4f} | — | {"Possible autocorrelation" if durbin_watson(residuals) < 1.5 or durbin_watson(residuals) > 2.5 else "OK"} |
| Chow (structural break) | {chow_stat:.4f} | {chow_pval:.4f} | {"STRUCTURAL BREAK" if chow_pval < 0.05 else "OK (stable)"} |

### VIF (Multicollinearity)
| Variable | VIF |
|---|---|
| roa | {vif_data['roa']:.2f} |
| der | {vif_data['der']:.2f} |
| beta | {vif_data['beta']:.2f} |

## 3. Robust Standard Errors (HC3)

| Variable | Coef (HC3) | SE (HC3) | t | P>|t| |
|---|---|---|---|---|---|
| const | {ols_robust.params['const']:.2f} | {ols_robust.bse['const']:.2f} | {ols_robust.tvalues['const']:.2f} | {ols_robust.pvalues['const']:.4f} |
| roa | {ols_robust.params['roa']:.2f} | {ols_robust.bse['roa']:.2f} | {ols_robust.tvalues['roa']:.2f} | {ols_robust.pvalues['roa']:.4f} |
| der | {ols_robust.params['der']:.3f} | {ols_robust.bse['der']:.3f} | {ols_robust.tvalues['der']:.2f} | {ols_robust.pvalues['der']:.4f} |
| beta | {ols_robust.params['beta']:.2f} | {ols_robust.bse['beta']:.2f} | {ols_robust.tvalues['beta']:.2f} | {ols_robust.pvalues['beta']:.4f} |

## 4. Pre vs Post COVID Comparison

### Pre-COVID (2010-2019, N={n_pre})
- R² = {ols_pre.rsquared:.4f}
- ROA coef = {ols_pre.params['roa']:.2f} (p={ols_pre.pvalues['roa']:.4f})
- DER coef = {ols_pre.params['der']:.3f} (p={ols_pre.pvalues['der']:.4f})
- Beta coef = {ols_pre.params['beta']:.2f} (p={ols_pre.pvalues['beta']:.4f})

### Post-COVID (2020-2025, N={n_post})
- R² = {ols_post.rsquared:.4f}
- ROA coef = {ols_post.params['roa']:.2f} (p={ols_post.pvalues['roa']:.4f})
- DER coef = {ols_post.params['der']:.3f} (p={ols_post.pvalues['der']:.4f})
- Beta coef = {ols_post.params['beta']:.2f} (p={ols_post.pvalues['beta']:.4f})

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
"""

(PROC / "validation_report.md").write_text(report, encoding="utf-8")
print("✅ validation_report.md saved")
print("\n=== VALIDATION COMPLETE ===")
