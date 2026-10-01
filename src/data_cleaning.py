"""
data_cleaning.py
------------------
Data cleaning utilities for the Global Superstore (2011-2014) dataset.

These functions encapsulate Phase 5 of the project:
- Parsing mixed-format date columns (validated via Ship Date >= Order Date)
- Feature engineering (Processing Time)
- Dropping non-analytical / mostly-empty columns
"""

import pandas as pd


def load_and_clean_data(filepath: str, encoding: str = "latin1") -> pd.DataFrame:
    """
    Load the raw Global Superstore CSV and return a fully cleaned DataFrame.

    Steps performed:
        1. Load raw CSV
        2. Parse 'Order Date' and 'Ship Date' (mixed DD/MM/YYYY and DD-MM-YYYY formats)
        3. Validate parsing logically (Ship Date must never precede Order Date)
        4. Engineer 'Processing Time' (days between order and shipment)
        5. Drop 'Row ID' (identifier only) and 'Postal Code' (~80% missing)

    Parameters
    ----------
    filepath : str
        Path to the raw superstore CSV file.
    encoding : str
        File encoding (the raw file requires 'latin1', not default utf-8).

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe ready for EDA and KPI calculation.
    """
    df = pd.read_csv(filepath, encoding=encoding)

    # --- Parse mixed-format dates ---
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, format="mixed")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True, format="mixed")

    # --- Validation: a shipment can never happen before the order was placed ---
    invalid_dates = (df["Ship Date"] < df["Order Date"]).sum()
    assert invalid_dates == 0, (
        f"Date parsing issue detected: {invalid_dates} rows have Ship Date "
        "before Order Date. Check the date format assumption."
    )

    # --- Feature engineering ---
    df["Processing Time"] = (df["Ship Date"] - df["Order Date"]).dt.days

    # --- Drop non-analytical / mostly-empty columns ---
    columns_to_drop = [c for c in ["Row ID", "Postal Code"] if c in df.columns]
    df = df.drop(columns=columns_to_drop)

    return df


def check_data_quality(df: pd.DataFrame) -> dict:
    """
    Run a quick data-quality summary on a (presumably cleaned) dataframe.
    Useful as a sanity check after load_and_clean_data().

    Returns
    -------
    dict with duplicate count, remaining nulls, and date range.
    """
    return {
        "shape": df.shape,
        "duplicates": int(df.duplicated().sum()),
        "nulls_remaining": df.isnull().sum()[df.isnull().sum() > 0].to_dict(),
        "order_date_range": (df["Order Date"].min(), df["Order Date"].max())
        if "Order Date" in df.columns
        else None,
    }


if __name__ == "__main__":
    # Quick manual test when running this file directly
    cleaned = load_and_clean_data("../data/raw/superstore_dataset2011-2015.csv")
    print(check_data_quality(cleaned))
