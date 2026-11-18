"""
matches_loader.py — Loads match data from v_matches_enriched view in football_dw.
Used by the statistics and chart entry points.
"""
import pandas as pd
from .db_utils.read_sql import read_sql_to_df
from .db_utils.convert_types import convert_enriched_types


def load_matches_df() -> pd.DataFrame:
    """
    Loads data from v_matches_enriched view in football_dw data warehouse.
    The view contains all match columns with joined dimensions (dim_date,
    dim_division, dim_team x2).
    Returns DataFrame with columns: Division, HomeTeam, AwayTeam, HomeElo, AwayElo,
    Form3Home, Form5Home, Form3Away, Form5Away, FTHome, FTAway, FTResult,
    HTHome, HTAway, HTResult, HomeShots, AwayShots, HomeTarget, AwayTarget,
    HomeFouls, AwayFouls, HomeCorners, AwayCorners, HomeYellow, AwayYellow,
    HomeRed, AwayRed, OddHome, OddDraw, OddAway, MaxHome, MaxDraw, MaxAway,
    Over25, Under25, MaxOver25, MaxUnder25, HandiSize, HandiHome, HandiAway,
    C_LTH, C_LTA, C_VHD, C_VAD, C_HTB, C_PHB, MatchDate
    """
    df = read_sql_to_df("SELECT * FROM v_matches_enriched")
    df = convert_enriched_types(df)
    return df
