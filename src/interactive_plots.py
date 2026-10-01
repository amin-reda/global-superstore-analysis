"""
interactive_plots.py
----------------------
Plotly interactive visualizations for the Global Superstore project.

WHY THIS IS A SEPARATE FILE:
This sandbox environment has no internet access, so `plotly` could not be
pip-installed or executed here to produce a static preview. The code below
is syntactically correct and ready to run in YOUR environment (Jupyter,
VS Code, etc.), where `pip install plotly` will work normally.

Run this file directly (`python interactive_plots.py`) or copy individual
functions into a notebook cell — each fig.show() opens an interactive
HTML chart in your browser / notebook output.
"""

import sys
sys.path.insert(0, ".")
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data_cleaning import load_and_clean_data
from rfm_analysis import segment_customers, segment_summary


def interactive_rfm_scatter(rfm_scored: pd.DataFrame):
    """Recency vs Frequency, bubble size = Monetary, colored by segment."""
    fig = px.scatter(
        rfm_scored.reset_index(),
        x="Recency", y="Frequency",
        color="RFM_Segment", size="Monetary",
        hover_name="Customer ID",
        title="Interactive RFM Segmentation: Recency vs Frequency",
        size_max=40, opacity=0.7,
    )
    fig.update_layout(width=950, height=600)
    return fig


def interactive_revenue_treemap(summary: pd.DataFrame):
    """Treemap of revenue contribution by RFM segment."""
    fig = px.treemap(
        summary.reset_index(),
        path=["RFM_Segment"], values="Total_Monetary",
        color="Avg_Monetary", color_continuous_scale="Blues",
        title="Revenue Contribution by Segment (Treemap)",
    )
    fig.update_layout(width=800, height=500)
    return fig


def interactive_discount_vs_profit(df: pd.DataFrame):
    """Interactive version of the discount-threshold chart (hover to inspect each bucket)."""
    bins = [-0.01, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.85]
    labels = ["0%", "0-10%", "10-20%", "20-30%", "30-40%",
              "40-50%", "50-60%", "60-70%", "70-85%"]
    df = df.copy()
    df["Discount_Bucket"] = pd.cut(df["Discount"], bins=bins, labels=labels)
    avg_profit = df.groupby("Discount_Bucket", observed=True)["Profit"].mean().reset_index()

    fig = px.bar(
        avg_profit, x="Discount_Bucket", y="Profit",
        color=avg_profit["Profit"] > 0,
        color_discrete_map={True: "#2ca02c", False: "#d62728"},
        title="Average Profit per Order by Discount Range (Interactive)",
        labels={"Profit": "Average Profit ($)", "Discount_Bucket": "Discount Range"},
    )
    fig.update_layout(showlegend=False, width=900, height=550)
    fig.add_hline(y=0, line_color="black")
    return fig


def interactive_market_category_heatmap(df: pd.DataFrame):
    """Heatmap of profit margin % across Market x Category (find where problems hide)."""
    pivot = df.pivot_table(
        values="Profit", index="Market", columns="Category", aggfunc="sum"
    ) / df.pivot_table(
        values="Sales", index="Market", columns="Category", aggfunc="sum"
    ) * 100

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values, x=pivot.columns, y=pivot.index,
        colorscale="RdYlGn", zmid=0,
        text=pivot.round(1).values, texttemplate="%{text}%",
    ))
    fig.update_layout(title="Profit Margin % — Market x Category", width=700, height=500)
    return fig


if __name__ == "__main__":
    df = load_and_clean_data("../data/raw/superstore_dataset2011-2015.csv")
    rfm_scored = segment_customers(df)
    summary = segment_summary(rfm_scored)

    interactive_rfm_scatter(rfm_scored).show()
    interactive_revenue_treemap(summary).show()
    interactive_discount_vs_profit(df).show()
    interactive_market_category_heatmap(df).show()
