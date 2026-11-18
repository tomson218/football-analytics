"""
elo_loader.py — Loads Elo time series from raw_eloRatings table in football_dw.
Used by charts/elo_time_series.py module.
"""
import pandas as pd
from .db_utils.read_sql import read_sql_to_df


def load_elo_timeseries_df() -> pd.DataFrame:
    """
    Loads Elo time series from raw_eloRatings table in football_dw data warehouse.
    Returns DataFrame with columns: MatchDate, club, elo.
    """
    query = """
        SELECT
            date    AS MatchDate,
            club    AS club,
            elo     AS elo
        FROM raw_eloRatings
    """

    df = read_sql_to_df(query)
    df['elo'] = pd.to_numeric(df['elo'], errors='coerce')
    df['MatchDate'] = pd.to_datetime(df['MatchDate'])
    return df
