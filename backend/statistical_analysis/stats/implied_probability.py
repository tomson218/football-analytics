"""
implied_probability.py — Implied probability from bookmaker odds.
"""
import pandas as pd
import numpy as np
from common.constants import AVG_ODDS_COLS


def odds_implied_probability(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates implied probability from bookmaker odds (1/odd).
    Returns DataFrame with mean implied probability and bookmaker margin.
    """
    available_cols = [col for col in AVG_ODDS_COLS if col in df.columns]

    if not available_cols:
        return pd.DataFrame()

    implied = pd.DataFrame()
    for col in available_cols:
        implied[f'Implied_{col}'] = 1 / df[col].replace(0, np.nan)

    implied['Total_Margin'] = implied.sum(axis=1)

    return implied.mean().to_frame('Mean Implied Prob')
