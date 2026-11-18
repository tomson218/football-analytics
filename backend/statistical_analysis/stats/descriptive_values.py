"""
descriptive_values.py — Descriptive statistics for numeric columns.
Min, max, mean, std, median, quartiles, quantiles.
"""
import pandas as pd


def calculate_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates descriptive statistics for all numeric columns:
    min, max, mean, std, median, Q1, Q3, quantiles 0.1 and 0.9.
    """
    numeric_cols = df.select_dtypes(include='number').columns

    stats = pd.DataFrame({
        'Minimum': df[numeric_cols].min(),
        'Maximum': df[numeric_cols].max(),
        'Mean': df[numeric_cols].mean(),
        'Std': df[numeric_cols].std(),
        'Median': df[numeric_cols].median(),
        'Quartile Q1': df[numeric_cols].quantile(0.25),
        'Quartile Q3': df[numeric_cols].quantile(0.75),
        'Quantile_0.1': df[numeric_cols].quantile(0.1),
        'Quantile_0.9': df[numeric_cols].quantile(0.9)
    })

    return stats
