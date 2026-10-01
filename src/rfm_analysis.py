"""
rfm_analysis.py
-----------------
Customer segmentation via RFM (Recency, Frequency, Monetary) analysis.

This complements the product/market-level findings (Phases 6-11) with a
customer-level lens: which customers are most valuable, which are slipping
away, and where a win-back campaign would have the highest ROI.
"""

import pandas as pd


def compute_rfm(df: pd.DataFrame,
                 customer_col: str = "Customer ID",
                 order_col: str = "Order ID",
                 date_col: str = "Order Date",
                 sales_col: str = "Sales") -> pd.DataFrame:
    """
    Build the base RFM table (one row per customer).

    Recency  = days since the customer's most recent order
               (relative to one day after the last date in the dataset)
    Frequency = number of distinct orders placed
    Monetary  = total sales value generated
    """
    snapshot_date = df[date_col].max() + pd.Timedelta(days=1)

    rfm = df.groupby(customer_col).agg(
        Recency=(date_col, lambda x: (snapshot_date - x.max()).days),
        Frequency=(order_col, "nunique"),
        Monetary=(sales_col, "sum"),
    )
    return rfm


def score_rfm(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Add 1-5 quintile scores for each dimension (5 = best) and an
    RFM_Score string (e.g. '531') useful for quick sorting/filtering.
    Lower Recency is better, so its scoring is reversed.
    """
    rfm = rfm.copy()
    rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["F_Score"] = pd.qcut(
        rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]
    ).astype(int)
    rfm["M_Score"] = pd.qcut(rfm["Monetary"], 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["RFM_Score"] = (
        rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)
    )
    rfm["RFM_Sum"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]
    return rfm


def _assign_segment(row) -> str:
    r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif r >= 3 and f >= 3 and m >= 3:
        return "Loyal Customers"
    elif r >= 4 and f <= 2:
        return "New Customers"
    elif r <= 2 and f >= 4 and m >= 4:
        return "At Risk (High Value)"
    elif r <= 2 and f <= 2 and m <= 2:
        return "Lost"
    elif r <= 2:
        return "Hibernating"
    else:
        return "Need Attention"


def segment_customers(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Full pipeline: compute RFM -> score it -> assign a business-readable segment.
    Returns one row per customer with Recency/Frequency/Monetary, scores, and Segment.
    """
    rfm = compute_rfm(df, **kwargs)
    rfm = score_rfm(rfm)
    rfm["RFM_Segment"] = rfm.apply(_assign_segment, axis=1)
    return rfm


def segment_summary(rfm_scored: pd.DataFrame) -> pd.DataFrame:
    """Aggregate stats per segment, sorted by total revenue contributed."""
    summary = rfm_scored.groupby("RFM_Segment").agg(
        Customers=("Recency", "count"),
        Avg_Recency_Days=("Recency", "mean"),
        Avg_Frequency=("Frequency", "mean"),
        Avg_Monetary=("Monetary", "mean"),
        Total_Monetary=("Monetary", "sum"),
    ).round(1)
    summary["Pct_of_Customers"] = (summary["Customers"] / summary["Customers"].sum() * 100).round(1)
    summary["Pct_of_Revenue"] = (summary["Total_Monetary"] / summary["Total_Monetary"].sum() * 100).round(1)
    return summary.sort_values("Total_Monetary", ascending=False)


if __name__ == "__main__":
    from data_cleaning import load_and_clean_data

    df = load_and_clean_data("../data/raw/superstore_dataset2011-2015.csv")
    rfm = segment_customers(df)
    print(segment_summary(rfm))
