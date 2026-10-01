"""
kpi_calculations.py
--------------------
KPI functions for the Global Superstore project (Phase 7).

Every function here returns a plain Python value (float / dict / DataFrame)
rather than printing, so they can be reused in notebooks, dashboards,
or unit tests.
"""

import pandas as pd


def total_revenue_and_profit(df: pd.DataFrame) -> dict:
    """KPI 1: Total Revenue & Total Profit."""
    return {
        "total_revenue": df["Sales"].sum(),
        "total_profit": df["Profit"].sum(),
    }


def overall_profit_margin(df: pd.DataFrame) -> float:
    """KPI 2: Overall Profit Margin (%)."""
    return df["Profit"].sum() / df["Sales"].sum() * 100


def average_order_value(df: pd.DataFrame, order_id_col: str = "Order ID") -> dict:
    """
    KPI 3: Average Order Value (AOV) — computed correctly at the ORDER level,
    not the line-item level (an Order ID can span multiple product rows).
    """
    order_totals = df.groupby(order_id_col)["Sales"].sum()
    return {
        "aov_mean": order_totals.mean(),
        "aov_median": order_totals.median(),
    }


def profit_margin_by_group(df: pd.DataFrame, group_col: str) -> pd.Series:
    """
    KPI 4 / 5: Profit Margin (%) grouped by any categorical column
    (e.g. 'Category', 'Sub-Category', 'Market', 'Region').
    """
    grouped = df.groupby(group_col).apply(
        lambda x: x["Profit"].sum() / x["Sales"].sum() * 100
    )
    return grouped.sort_values()


def high_discount_impact(df: pd.DataFrame, threshold: float = 0.20) -> dict:
    """
    KPI 6: High-Discount Order Share & Profit Impact.
    Quantifies the financial cost of orders discounted above `threshold`.
    """
    high_disc = df[df["Discount"] > threshold]
    losing_orders = high_disc[high_disc["Profit"] < 0]
    return {
        "threshold": threshold,
        "high_discount_orders": len(high_disc),
        "share_of_all_orders_pct": len(high_disc) / len(df) * 100,
        "net_profit_of_group": high_disc["Profit"].sum(),
        "pct_of_group_losing_money": len(losing_orders) / len(high_disc) * 100
        if len(high_disc) > 0
        else 0,
    }


def sales_cagr(df: pd.DataFrame, date_col: str = "Order Date") -> float:
    """
    KPI 7: Compound Annual Growth Rate (CAGR) of Sales,
    computed from the first to the last full year in the data.
    """
    yearly_sales = df.groupby(df[date_col].dt.year)["Sales"].sum()
    first_year, last_year = yearly_sales.index.min(), yearly_sales.index.max()
    n_years = last_year - first_year
    cagr = (yearly_sales[last_year] / yearly_sales[first_year]) ** (1 / n_years) - 1
    return cagr * 100


def kpi_summary(df: pd.DataFrame) -> dict:
    """Convenience function: compute all 7 KPIs at once and return as a dict."""
    rev_profit = total_revenue_and_profit(df)
    aov = average_order_value(df)
    high_disc = high_discount_impact(df)

    return {
        "total_revenue": rev_profit["total_revenue"],
        "total_profit": rev_profit["total_profit"],
        "overall_margin_pct": overall_profit_margin(df),
        "aov_mean": aov["aov_mean"],
        "aov_median": aov["aov_median"],
        "category_margin_pct": profit_margin_by_group(df, "Category").to_dict(),
        "market_margin_pct": profit_margin_by_group(df, "Market").to_dict(),
        "high_discount_share_pct": high_disc["share_of_all_orders_pct"],
        "high_discount_net_profit": high_disc["net_profit_of_group"],
        "sales_cagr_pct": sales_cagr(df),
    }


if __name__ == "__main__":
    import json
    from data_cleaning import load_and_clean_data

    cleaned = load_and_clean_data("../data/raw/superstore_dataset2011-2015.csv")
    summary = kpi_summary(cleaned)
    print(json.dumps(summary, indent=2, default=str))
