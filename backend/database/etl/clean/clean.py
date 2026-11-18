"""
clean.py — Clean match data in memory before loading the data warehouse.
Invalid values are replaced column by column; records without a result are dropped.
"""
import pandas as pd

from common.constants import NUMERIC_COLS, MATCH_STATS_COLS, ODDS_COLS, PROB_COLS

KEY_COLS = ['FTHome', 'FTAway', 'FTResult', 'HTHome', 'HTAway', 'HTResult', 'HomeTeam', 'AwayTeam']


def rounded_mean(series):
    return int(round(series.mean()))


def replace_invalid(df, cols, fill, is_invalid=pd.Series.isna, as_int=False):
    """Replace invalid values in `cols` with `fill(column)`, optionally casting to int."""
    for col in cols:
        if col not in df.columns:
            continue
        df.loc[is_invalid(df[col]), col] = fill(df[col])
        if as_int:
            df[col] = df[col].astype(int)


def outside(low, high):
    """Build a check for values that are missing or outside [low, high]."""
    return lambda series: series.isna() | (series < low) | (series > high)


def clean(df_matches, df_elo):
    """Main clean function — returns cleaned DataFrames."""
    print('3. Cleaning data...')

    for col in NUMERIC_COLS:
        if col in df_matches.columns:
            df_matches[col] = pd.to_numeric(df_matches[col], errors='coerce')

    mean, median = pd.Series.mean, pd.Series.median
    replace_invalid(df_matches, ['HomeElo', 'AwayElo'], mean)
    replace_invalid(df_matches, ['Form3Home', 'Form3Away'], rounded_mean, outside(0, 9), as_int=True)
    replace_invalid(df_matches, ['Form5Home', 'Form5Away'], rounded_mean, outside(0, 15), as_int=True)
    replace_invalid(df_matches, MATCH_STATS_COLS, rounded_mean, as_int=True)
    replace_invalid(df_matches, ODDS_COLS, median, lambda s: s.isna() | (s < 1.0))
    replace_invalid(df_matches, ['HandiSize'], mean)
    replace_invalid(df_matches, ['HandiHome', 'HandiAway'], mean, lambda s: s.isna() | (s < 0))
    replace_invalid(df_matches, PROB_COLS, median, outside(0.0001, 0.9999))

    df_matches = df_matches.dropna(subset=KEY_COLS, how='any')

    print(f'   After cleaning: {len(df_matches)} matches.')
    print(f'   Elo data in raw_eloRatings (DW): {len(df_elo)} records.')

    return df_matches, df_elo
