"""
common/constants.py — Central repository for ETL, ML and statistical analysis constants.
"""

# ---------------------------------------------------------------------------
# ML feature columns (CatBoost HomeNoLose models)
# ---------------------------------------------------------------------------

# All 25 numerical features from matches_cleaned.csv (base model)
FEATURE_COLS_BASE = [
    'C_LTA', 'HomeElo', 'AwayElo',
    'Form3Home', 'Form5Home', 'Form3Away', 'Form5Away',
    'OddDraw', 'OddAway', 'OddHome',
    'MaxHome', 'MaxDraw', 'MaxAway',
    'Over25', 'Under25', 'MaxOver25', 'MaxUnder25',
    'HandiSize', 'HandiHome', 'HandiAway',
    'C_LTH', 'C_VHD', 'C_VAD', 'C_PHB', 'C_HTB'
]

# 10-feature model (top features by importance from base model)
FEATURE_COLS_10 = [
    'OddHome', 'MaxAway', 'MaxHome',
    'OddAway', 'OddDraw', 'MaxDraw',
    'HandiSize', 'HandiHome',
    'C_HTB', 'C_LTA'
]

# 6-feature model (top 6 features by importance from base model)
FEATURE_COLS_6 = [
    'OddHome', 'OddAway', 'MaxAway',
    'HandiSize', 'MaxHome', 'MaxDraw'
]

# ---------------------------------------------------------------------------
# ETL configuration
# ---------------------------------------------------------------------------

# Top leagues to filter
TOP_LEAGUES = ['I1', 'SP1', 'D1', 'F1', 'N1']

# Date range
START_DATE = '2020-08-01'
END_DATE = '2025-06-30'

# Division to country mapping
DIVISION_TO_COUNTRY = {
    'I1': 'ITA',
    'SP1': 'ESP',
    'D1': 'GER',
    'F1': 'FRA',
    'N1': 'NED'
}

# League display names
LEAGUE_NAMES = {
    'I1': 'Serie A',
    'SP1': 'La Liga',
    'D1': 'Bundesliga',
    'F1': 'Ligue 1',
    'N1': 'Eredivisie'
}

# Batch insert size
BATCH_SIZE = 1000

# Day and month names (for dim_date)
DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

MONTH_NAMES = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# Numeric columns in raw_Matches
NUMERIC_COLS = [
    'HomeElo', 'AwayElo',
    'Form3Home', 'Form5Home', 'Form3Away', 'Form5Away',
    'FTHome', 'FTAway', 'HTHome', 'HTAway',
    'HomeShots', 'AwayShots', 'HomeTarget', 'AwayTarget',
    'HomeFouls', 'AwayFouls', 'HomeCorners', 'AwayCorners',
    'HomeYellow', 'AwayYellow', 'HomeRed', 'AwayRed',
    'OddHome', 'OddDraw', 'OddAway',
    'MaxHome', 'MaxDraw', 'MaxAway',
    'Over25', 'Under25', 'MaxOver25', 'MaxUnder25',
    'HandiSize', 'HandiHome', 'HandiAway',
    'C_LTH', 'C_LTA', 'C_VHD', 'C_VAD', 'C_HTB', 'C_PHB'
]

# Match statistics columns (int)
MATCH_STATS_COLS = [
    'HomeShots', 'AwayShots', 'HomeTarget', 'AwayTarget',
    'HomeFouls', 'AwayFouls', 'HomeCorners', 'AwayCorners',
    'HomeYellow', 'AwayYellow', 'HomeRed', 'AwayRed'
]

# Odds columns (all 10)
ODDS_COLS = [
    'OddHome', 'OddDraw', 'OddAway',
    'MaxHome', 'MaxDraw', 'MaxAway',
    'Over25', 'Under25', 'MaxOver25', 'MaxUnder25'
]

# Average and maximum 1X2 odds columns (used for odds distribution)
ODDS_1X2_COLS = ['OddHome', 'OddDraw', 'OddAway', 'MaxHome', 'MaxDraw', 'MaxAway']

# Average odds columns (3 — used for implied probability)
AVG_ODDS_COLS = ['OddHome', 'OddDraw', 'OddAway']

# Probability columns
PROB_COLS = ['C_LTH', 'C_LTA', 'C_VHD', 'C_VAD', 'C_HTB', 'C_PHB']

# raw_Matches columns for INSERT
RAW_MATCHES_COLUMNS = [
    'id', 'Division', 'MatchDate', 'MatchTime', 'HomeTeam', 'AwayTeam',
    'HomeElo', 'AwayElo', 'Form3Home', 'Form5Home', 'Form3Away', 'Form5Away',
    'FTHome', 'FTAway', 'FTResult', 'HTHome', 'HTAway', 'HTResult',
    'HomeShots', 'AwayShots', 'HomeTarget', 'AwayTarget',
    'HomeFouls', 'AwayFouls', 'HomeCorners', 'AwayCorners',
    'HomeYellow', 'AwayYellow', 'HomeRed', 'AwayRed',
    'OddHome', 'OddDraw', 'OddAway',
    'MaxHome', 'MaxDraw', 'MaxAway',
    'Over25', 'Under25', 'MaxOver25', 'MaxUnder25',
    'HandiSize', 'HandiHome', 'HandiAway',
    'C_LTH', 'C_LTA', 'C_VHD', 'C_VAD', 'C_HTB', 'C_PHB'
]

# ---------------------------------------------------------------------------
# Data loader column groups (used by statistical_analysis data_loaders)
# ---------------------------------------------------------------------------

# All numeric columns from v_matches_enriched view
ENRICHED_NUMERIC_COLS = NUMERIC_COLS

# Form columns that should be cast to int
ENRICHED_FORM_INT_COLS = ['Form3Home', 'Form3Away', 'Form5Home', 'Form5Away']

# Match statistics columns that should be cast to int
ENRICHED_MATCH_STATS_COLS = ['FTHome', 'FTAway', 'HTHome', 'HTAway'] + MATCH_STATS_COLS
