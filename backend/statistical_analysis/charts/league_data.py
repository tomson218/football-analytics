"""
league_data.py — Per-league data shared by the league charts.
"""
import pandas as pd

from common.constants import LEAGUE_NAMES


def league_labels(divisions) -> list:
    """Display names for division codes."""
    return [LEAGUE_NAMES.get(div, div) for div in divisions]


def teams_per_league(df: pd.DataFrame) -> tuple:
    """Return league labels and the number of distinct teams in each league."""
    divisions = df['Division'].unique()
    counts = []
    for div in divisions:
        df_div = df[df['Division'] == div]
        counts.append(len(set(df_div['HomeTeam']).union(df_div['AwayTeam'])))
    return league_labels(divisions), counts


def home_away_values_per_league(df: pd.DataFrame, home_col: str, away_col: str) -> tuple:
    """Return league labels and the combined home + away values for each league."""
    divisions = df['Division'].unique()
    values = []
    for div in divisions:
        df_div = df[df['Division'] == div]
        values.append(df_div[home_col].dropna().tolist() + df_div[away_col].dropna().tolist())
    return league_labels(divisions), values
