"""
load_fact_matches.py — Load fact_matches from cleaned data.
"""
import pandas as pd

from common.constants import DIVISION_TO_COUNTRY, BATCH_SIZE


def safe_float(val):
    return None if pd.isna(val) else float(val)


def safe_int(val):
    return 0 if pd.isna(val) else int(val)


def safe_str(val):
    return None if pd.isna(val) else str(val)


KEY_COLUMNS = ['date_key', 'home_team_key', 'away_team_key', 'division_key', 'season_key']

# fact_matches column -> (cleaned DataFrame column, converter)
MEASURES = {
    'home_elo': ('HomeElo', safe_float),
    'away_elo': ('AwayElo', safe_float),
    'form3_home': ('Form3Home', safe_int),
    'form5_home': ('Form5Home', safe_int),
    'form3_away': ('Form3Away', safe_int),
    'form5_away': ('Form5Away', safe_int),
    'ft_home_goals': ('FTHome', safe_int),
    'ft_away_goals': ('FTAway', safe_int),
    'ft_result': ('FTResult', safe_str),
    'ht_home_goals': ('HTHome', safe_int),
    'ht_away_goals': ('HTAway', safe_int),
    'ht_result': ('HTResult', safe_str),
    'home_shots': ('HomeShots', safe_int),
    'away_shots': ('AwayShots', safe_int),
    'home_target': ('HomeTarget', safe_int),
    'away_target': ('AwayTarget', safe_int),
    'home_fouls': ('HomeFouls', safe_int),
    'away_fouls': ('AwayFouls', safe_int),
    'home_corners': ('HomeCorners', safe_int),
    'away_corners': ('AwayCorners', safe_int),
    'home_yellow': ('HomeYellow', safe_int),
    'away_yellow': ('AwayYellow', safe_int),
    'home_red': ('HomeRed', safe_int),
    'away_red': ('AwayRed', safe_int),
    'odd_home': ('OddHome', safe_float),
    'odd_draw': ('OddDraw', safe_float),
    'odd_away': ('OddAway', safe_float),
    'max_home': ('MaxHome', safe_float),
    'max_draw': ('MaxDraw', safe_float),
    'max_away': ('MaxAway', safe_float),
    'odd_over_25': ('Over25', safe_float),
    'odd_under_25': ('Under25', safe_float),
    'max_over_25': ('MaxOver25', safe_float),
    'max_under_25': ('MaxUnder25', safe_float),
    'handi_size': ('HandiSize', safe_float),
    'handi_home': ('HandiHome', safe_float),
    'handi_away': ('HandiAway', safe_float),
    'c_lth': ('C_LTH', safe_float),
    'c_lta': ('C_LTA', safe_float),
    'c_vhd': ('C_VHD', safe_float),
    'c_vad': ('C_VAD', safe_float),
    'c_htb': ('C_HTB', safe_float),
    'c_phb': ('C_PHB', safe_float),
}

COLUMNS = KEY_COLUMNS + list(MEASURES)
INSERT_SQL = (
    f"INSERT INTO fact_matches ({', '.join(COLUMNS)}) "
    f"VALUES ({', '.join(['%s'] * len(COLUMNS))})"
)


def build_fact_record(row, dimension_maps):
    """Return the fact_matches record for a match, or None if a dimension key is missing."""
    div = row['Division']
    country_code = DIVISION_TO_COUNTRY.get(div, 'GER')
    team_keys = dimension_maps['team_id_cache']

    division_key = dimension_maps['division_code_to_key'].get(div)
    home_team_key = team_keys.get((row['HomeTeam'], country_code))
    away_team_key = team_keys.get((row['AwayTeam'], country_code))

    match_date = pd.to_datetime(row.get('MatchDate'), errors='coerce')
    if pd.isna(match_date):
        return None
    match_date = match_date.date()

    date_key = dimension_maps['date_to_key'].get(match_date)
    season_name = dimension_maps['date_to_season'].get(match_date)
    season_key = dimension_maps['season_name_to_key'].get(season_name) if season_name else None

    keys = (date_key, home_team_key, away_team_key, division_key, season_key)
    if any(key is None for key in keys):
        return None

    return keys + tuple(convert(row.get(col)) for col, convert in MEASURES.values())


def load_fact_matches(cnx, cursor, df_matches, dimension_maps):
    """STEP 10: Load fact_matches from cleaned data."""
    print('10. Loading fact_matches...')

    inserted = 0
    for idx in range(0, len(df_matches), BATCH_SIZE):
        batch_df = df_matches.iloc[idx:idx + BATCH_SIZE]
        records = [build_fact_record(row, dimension_maps) for _, row in batch_df.iterrows()]
        fact_records = [record for record in records if record is not None]

        if fact_records:
            cursor.executemany(INSERT_SQL, fact_records)
            cnx.commit()
            inserted += len(fact_records)
            print(f'   Loaded {inserted}/{len(df_matches)} matches.')

    print(f'   Total loaded {inserted} matches to fact_matches.')
    return inserted
