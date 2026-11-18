"""
common/constants.py — Central repository for ETL constants.
"""

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
