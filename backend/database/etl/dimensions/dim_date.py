"""
dim_date.py — Load dim_date with date attributes.
"""
import pandas as pd
from datetime import date, timedelta


def load_dim_date(cnx, cursor, df_matches, date_to_season, batch_size, day_names, month_names):
    """STEP 9: Load dim_date."""
    print('9. Loading dim_date...')

    match_dates = pd.to_datetime(df_matches['MatchDate'], errors='coerce').dropna()
    min_date = match_dates.min().date()
    max_date = match_dates.max().date()

    date_records = []
    current_date = min_date
    while current_date <= max_date:
        date_key = int(current_date.strftime('%Y%m%d'))
        year = current_date.year
        quarter = (current_date.month - 1) // 3 + 1
        month = current_date.month
        day = current_date.day
        day_of_week = current_date.weekday()
        day_name = day_names[day_of_week]
        month_name = month_names[month - 1]
        season_name = date_to_season.get(current_date)
        is_weekend = 1 if day_of_week >= 5 else 0
        is_weekday = 1 if day_of_week < 5 else 0

        date_records.append((
            date_key, current_date, year, quarter, month, day,
            day_of_week, day_name, month_name, season_name,
            is_weekend, is_weekday
        ))
        current_date += timedelta(days=1)

    for i in range(0, len(date_records), batch_size):
        batch = date_records[i:i + batch_size]
        cursor.executemany("""
            INSERT INTO dim_date (
                date_key, full_date, year, quarter, month, day,
                day_of_week, day_name, month_name, season_name,
                is_weekend, is_weekday
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, batch)
        cnx.commit()
    print(f'   Loaded {len(date_records)} dates.')

    # Build map: date -> date_key
    date_to_key = {}
    cursor.execute("SELECT date_key, full_date FROM dim_date")
    for dk, fd in cursor.fetchall():
        date_to_key[fd] = dk

    return date_to_key
