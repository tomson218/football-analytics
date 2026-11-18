"""
export_dimensions.py — Export 5 dimension tables to backend/csv/clean/.
"""
import os

from fetch_df import fetch_df

DIMENSION_TABLES = ['dim_country', 'dim_division', 'dim_team', 'dim_season', 'dim_date']


def export_dimension_tables(cursor, clean_csv_dir):
    """STEP 11: Export 5 dimension tables to backend/csv/clean/."""
    print('11. Exporting dimension tables to backend/csv/clean/...')
    os.makedirs(clean_csv_dir, exist_ok=True)

    for table in DIMENSION_TABLES:
        df = fetch_df(cursor, f"SELECT * FROM {table}")
        df.to_csv(os.path.join(clean_csv_dir, f'{table}.csv'), index=False)
        print(f'   {table}: {len(df)} records')
