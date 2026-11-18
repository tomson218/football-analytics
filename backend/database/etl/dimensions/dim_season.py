"""
dim_season.py — Load dim_season and generate season mappings.
"""
import pandas as pd
from datetime import date, timedelta


def load_dim_season(cnx, cursor, df_matches):
    """STEP 8: Load dim_season."""
    print('8. Loading dim_season...')

    match_dates = pd.to_datetime(df_matches['MatchDate'], errors='coerce').dropna()
    min_date = match_dates.min().date()
    max_date = match_dates.max().date()

    def generate_seasons(min_d, max_d):
        seasons = []
        start_year = min_d.year
        if min_d.month <= 6:
            start_year = min_d.year - 1
        end_year_limit = max_d.year
        year = start_year
        while year <= end_year_limit:
            season_name = f"{year}/{str(year + 1)[-2:]}"
            season_start = date(year, 8, 1)
            season_end = date(year + 1, 6, 30)
            seasons.append((season_name, year, year + 1, season_start, season_end))
            year += 1
        return seasons

    seasons = generate_seasons(min_date, max_date)
    for season_name, start_year, end_year, start_date, end_date in seasons:
        cursor.execute("""
            INSERT INTO dim_season (season_name, start_year, end_year, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (season_name, start_year, end_year, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    cnx.commit()
    print(f'   Loaded {len(seasons)} seasons.')

    season_name_to_key = {}
    cursor.execute("SELECT season_key, season_name FROM dim_season")
    for sk, sn in cursor.fetchall():
        season_name_to_key[sn] = sk

    # Build map: date -> season_name
    date_to_season = {}
    for season_name, start_year, end_year, start_date, end_date in seasons:
        current = start_date
        while current <= end_date:
            if current not in date_to_season:
                date_to_season[current] = season_name
            current += timedelta(days=1)

    return seasons, season_name_to_key, date_to_season
