# Global Superstore Profitability Analysis (2011–2014)

A complete end-to-end data analysis project on the Global Superstore dataset (~51K orders),
built to answer one central business question: **does sales volume actually translate into
profit — and if not, where exactly does it break down?**

## Business Problem

The company's sales are growing strongly across markets, but it isn't clear whether that
growth is translating into proportional profit, or which regions/categories/customer
segments are genuinely profitable versus which ones are losing money despite healthy sales.

## Key Insights

1. **Discount is the root cause of the company's weakest profitability points.** Orders
   discounted above ~20% lose money in 89.9% of cases, costing the company a net
   **-$814,682** across 11,328 orders (22.1% of all orders).
2. **Tables (Furniture sub-category)** loses -$64,083 overall, driven entirely by orders
   discounted above 20% (avg. discount on Tables = 29.1%, double the company average).
   The same product is profitable wherever discounting stays under 20%.
3. **EMEA** is the weakest market by profit margin (5.4% vs. ~11–13% elsewhere), driven by
   a systemically higher average discount rate (19.6%) applied across *all* categories —
   not a single product issue.
4. Company-wide growth is healthy: Sales CAGR of 23.9% (2011–2014) with a stable overall
   margin (~11–12%) — the issues above are localized, not systemic to the whole business.
5. Ship Mode / Processing Time were tested and ruled out as drivers of profitability
   (correlation ≈ 0).
6. **RFM customer segmentation:** Champions (21.8% of customers) generate 43.3% of total
   revenue; "Lost" is the largest segment by headcount (367 customers) but only 3.6% of
   revenue. The "At Risk (High Value)" segment (77 customers, 9.1% of revenue) was tested
   against the discount hypothesis and — unlike Tables/EMEA — their churn is **not**
   discount-driven (they actually received the *lowest* average discount), flagging a
   genuine open question for further investigation (satisfaction, competition, etc.).

## Methodology

1. **Data Cleaning** — parsed mixed-format date columns (validated via the logical rule
   `Ship Date >= Order Date`), engineered `Processing Time`, dropped non-analytical columns.
2. **EDA** — univariate, bivariate, and multivariate analysis across Sales, Profit,
   Discount, Category, Market, and Ship Mode.
3. **KPI Design** — 7 KPIs derived directly from EDA findings (not decided upfront).
4. **Insight Discovery & Validation** — every insight tested against sample size,
   outlier influence, and correlation-vs-causation before being accepted.
5. **RFM Segmentation** — customer-level lens (Recency, Frequency, Monetary) layered on
   top of the product/market findings.
6. **Recommendations** — each tied explicitly to a specific insight and its evidence.

## Project Structure

```text
global-superstore-analysis/
├── data/
│   ├── raw/                 # original, untouched CSV
│   └── processed/           # cleaned dataset used for all analysis
├── notebooks/                # 01 cleaning -> 05 RFM segmentation
├── src/                       # reusable cleaning / KPI / RFM / plotting functions
├── visualizations/            # exported chart PNGs (matplotlib/seaborn)
├── presentation/              # final .pptx + speaker notes
├── requirements.txt
└── README.md
```

## How to Run

```bash
pip install -r requirements.txt
jupyter notebook notebooks/01_data_cleaning.ipynb
```

Or use the `src/` modules directly:

```python
from src.data_cleaning import load_and_clean_data
from src.kpi_calculations import kpi_summary
from src.rfm_analysis import segment_customers, segment_summary

df = load_and_clean_data("data/raw/superstore_dataset2011-2015.csv")
print(kpi_summary(df))
print(segment_summary(segment_customers(df)))
```

For interactive Plotly charts, run `python src/interactive_plots.py` (requires
`pip install plotly`, not needed for the rest of the project).

## Tools

Python · Pandas · NumPy · Matplotlib · Seaborn · Plotly · Jupyter
