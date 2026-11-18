"""
convert_types.py — Convert column types for v_matches_enriched data.
"""
import pandas as pd

from common.constants import (
    ENRICHED_NUMERIC_COLS,
    ENRICHED_FORM_INT_COLS,
    ENRICHED_MATCH_STATS_COLS,
)


def convert_enriched_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert column types for data loaded from v_matches_enriched view.
    Uses constants from common.constants for column lists.
    """
    # Convert numeric columns (from Decimal to float)
    for col in ENRICHED_NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Form and match statistics columns as int
    for col in ENRICHED_FORM_INT_COLS + ENRICHED_MATCH_STATS_COLS:
        if col in df.columns:
            df[col] = df[col].astype(int)

    return df
