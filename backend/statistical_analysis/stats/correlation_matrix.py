"""
correlation_matrix.py — Pearson correlation matrix for all numeric variables.
"""
import numpy as np
import pandas as pd


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates and returns Pearson correlation matrix for all
    numeric variables in DataFrame.
    """
    numeric_df = df.select_dtypes(include=np.number)
    corr_matrix = numeric_df.corr()
    return corr_matrix
