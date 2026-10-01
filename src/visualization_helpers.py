"""
visualization_helpers.py
--------------------------
Reusable plotting functions so every chart in the project shares
the same style (Phase 9: Visualization Strategy).

Each function saves the figure to /visualizations/ and also returns
the matplotlib Axes object in case further customization is needed.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
FIGURE_DIR = os.path.join(os.path.dirname(__file__), "..", "visualizations")


def _save(fig, filename):
    os.makedirs(FIGURE_DIR, exist_ok=True)
    fig.savefig(os.path.join(FIGURE_DIR, filename), dpi=150, bbox_inches="tight")


def plot_margin_by_group(margin_series, title, filename, xlabel="Profit Margin (%)"):
    """
    Horizontal bar chart of profit margin by category/market/sub-category.
    Use for KPI 4 and KPI 5.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#d62728" if v < 0 else "#1f77b4" for v in margin_series.values]
    margin_series.plot(kind="barh", ax=ax, color=colors)
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.axvline(0, color="black", linewidth=0.8)
    _save(fig, filename)
    return ax


def plot_discount_vs_profit(df, filename="discount_vs_profit.png"):
    """
    Bar chart: average profit per order across discount buckets.
    This is the chart behind the project's central insight
    (profit turns negative beyond ~20% discount).
    """
    bins = [-0.01, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.85]
    labels = ["0%", "0-10%", "10-20%", "20-30%", "30-40%",
              "40-50%", "50-60%", "60-70%", "70-85%"]
    bucket = pd.cut(df["Discount"], bins=bins, labels=labels)
    avg_profit = df.groupby(bucket)["Profit"].mean()

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = ["#d62728" if v < 0 else "#2ca02c" for v in avg_profit.values]
    avg_profit.plot(kind="bar", ax=ax, color=colors)
    ax.set_title("Average Profit per Order by Discount Range", fontsize=13, fontweight="bold")
    ax.set_ylabel("Average Profit ($)")
    ax.set_xlabel("Discount Range")
    ax.axhline(0, color="black", linewidth=0.8)
    plt.xticks(rotation=45)
    _save(fig, filename)
    return ax


def plot_yearly_trend(df, date_col="Order Date", filename="sales_growth_trend.png"):
    """Line chart: Sales & Profit over time (Phase 6, temporal analysis)."""
    yearly = df.groupby(df[date_col].dt.year).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))

    fig, ax = plt.subplots(figsize=(8, 5))
    yearly["Sales"].plot(ax=ax, marker="o", label="Sales")
    yearly["Profit"].plot(ax=ax, marker="o", label="Profit", secondary_y=False)
    ax.set_title("Sales & Profit Growth (2011-2014)", fontsize=13, fontweight="bold")
    ax.set_ylabel("USD")
    ax.legend()
    _save(fig, filename)
    return ax


def plot_sales_distribution(df, filename="sales_distribution.png"):
    """Histogram of Sales, useful to show the right-skew discussed in Univariate EDA."""
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["Sales"], bins=60, ax=ax, color="#1f77b4")
    ax.set_title("Sales Distribution (Right-Skewed)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Sales ($)")
    _save(fig, filename)
    return ax

