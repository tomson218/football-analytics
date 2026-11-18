"""
odds_distribution.py — Bookmaker odds distribution statistics.
"""
import pandas as pd
from common.constants import ODDS_1X2_COLS


def odds_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates bookmaker odds distribution:
    OddHome, OddDraw, OddAway, MaxHome, MaxDraw, MaxAway.
    Returns DataFrame with min, max, mean, median and std.
    """
    available_cols = [col for col in ODDS_1X2_COLS if col in df.columns]

    if not available_cols:
        return pd.DataFrame()

    stats = pd.DataFrame({
        'Minimum': df[available_cols].min(),
        'Maximum': df[available_cols].max(),
        'Mean': df[available_cols].mean(),
        'Median': df[available_cols].median(),
        'Std': df[available_cols].std(),
    })

    return stats
