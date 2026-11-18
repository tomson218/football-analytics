"""
export_raw.py — Export raw data to backend/csv/raw/.
"""
import os

from fetch_df import fetch_df

RAW_EXPORTS = [
    ('raw_eloRatings', 'raw Elo records', "SELECT date, club, country, elo FROM raw_eloRatings"),
    ('raw_Matches', 'raw matches', "SELECT * FROM raw_Matches"),
]


def export_raw_data(cursor, raw_csv_dir):
    """STEP 2c: Export raw data to backend/csv/raw/."""
    print('2c. Exporting raw data to backend/csv/raw/...')
    os.makedirs(raw_csv_dir, exist_ok=True)

    for table, label, query in RAW_EXPORTS:
        df = fetch_df(cursor, query)
        path = os.path.join(raw_csv_dir, f'{table}.csv')
        df.to_csv(path, index=False)
        print(f'   Saved {len(df)} {label} to {path}')
