"""
run_stats.py — Entry point for descriptive statistics.
Loads data from DB and runs all statistical functions.
"""
import pandas as pd

from .data_loaders import load_matches_df
from .stats import calculate_values, pearson_correlation, linear_regression, correlation_matrix


def descriptive_stats_all():
    """Loads data from DB and prints all descriptive statistics."""
    print("Loading data from MySQL database...")
    df = load_matches_df()
    print(f"Loaded {len(df)} matches.\n")

    # 1. Descriptive statistics
    stats = calculate_values(df)
    print("=== DESCRIPTIVE STATISTICS ===")
    print(stats.round(4))
    print()

    # 2. Pearson correlation
    r, p_value = pearson_correlation(df)
    print(f"Correlation coefficient r (HT result influence on final match result) = {r:.4f}")
    print(f"P-value = {p_value:.4f}\n")

    # 3. Linear regression
    a, b = linear_regression(df)
    print(f"Regression formula: Y = {a:.4f} * X + {b:.4f}\n")

    # 4. Correlation matrix
    matrix = correlation_matrix(df)
    print("=== CORRELATION MATRIX ===")
    print(matrix.round(4))

    # Save correlation matrix to Excel
    output_path = "./correlation_matrix.xlsx"
    matrix.to_excel(output_path, sheet_name='Correlations', float_format="%.4f")
    print(f"\nCorrelation matrix saved to Excel file: {output_path}")

    return df, stats, (r, p_value), (a, b), matrix


if __name__ == '__main__':
    descriptive_stats_all()
