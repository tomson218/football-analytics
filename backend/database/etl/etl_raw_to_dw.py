"""
etl_raw_to_dw.py — Main ETL script for football_dw data warehouse.

Flow:
  1. Raw CSV files (eloRatings.csv, Matches.csv) → raw_eloRatings + raw_Matches (football_dw)
  2. Clean data from raw_* tables in memory (pandas)
  3. Clean data → 5 dimension tables + 1 fact table (data warehouse)
  4. CSV export: raw data to csv/raw/, dimensions to csv/clean/

Run first: main_dw_db.py (creates schema), then this script.
"""
import mysql.connector
import os
import sys

# Add backend/, database/ and etl/ subfolders to path
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
database_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
etl_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)
sys.path.insert(0, database_dir)
sys.path.insert(0, etl_dir)
sys.path.insert(0, os.path.join(etl_dir, 'extract'))
sys.path.insert(0, os.path.join(etl_dir, 'clean'))
sys.path.insert(0, os.path.join(etl_dir, 'dimensions'))
sys.path.insert(0, os.path.join(etl_dir, 'facts'))
sys.path.insert(0, os.path.join(etl_dir, 'export'))
from db_config import get_db_config

# Import ETL modules from subfolders
from common.constants import TOP_LEAGUES, START_DATE, END_DATE, BATCH_SIZE, RAW_MATCHES_COLUMNS

from truncate_raw import truncate_raw_tables
from load_raw_elo import load_raw_elo
from load_raw_matches import load_raw_matches
from clean import clean
from load_dimensions import load_dimensions
from load_fact_matches import load_fact_matches
from fetch_df import fetch_df
from export_raw import export_raw_data
from export_dimensions import export_dimension_tables
from print_summary import print_summary


def main():
    # ============================================================
    # Connect to database (from .env via db_config)
    # ============================================================
    print('Connecting to football_dw database...')
    dw_config = get_db_config()
    dw_cnx = mysql.connector.connect(**dw_config, use_pure=True)
    dw_cur = dw_cnx.cursor()

    # CSV paths (csv/ is in backend/)
    # backend_dir is already set at module level
    csv_dir = os.path.join(backend_dir, 'csv', 'raw')
    raw_csv_dir = csv_dir
    clean_csv_dir = os.path.join(backend_dir, 'csv', 'clean')

    # ============================================================
    # STEP 1-2: Extract raw data
    # ============================================================
    truncate_raw_tables(dw_cnx, dw_cur)
    print('2. Loading raw data from CSV to football_dw...')
    elo_count = load_raw_elo(dw_cnx, dw_cur, csv_dir, START_DATE, END_DATE, BATCH_SIZE)
    match_count = load_raw_matches(dw_cnx, dw_cur, csv_dir, TOP_LEAGUES, START_DATE, END_DATE, BATCH_SIZE, RAW_MATCHES_COLUMNS)

    # ============================================================
    # STEP 2c: Export raw data to CSV
    # ============================================================
    export_raw_data(dw_cur, raw_csv_dir)

    # ============================================================
    # STEP 3: Clean data
    # ============================================================
    df_matches = fetch_df(dw_cur, "SELECT * FROM raw_Matches")
    df_elo = fetch_df(dw_cur, "SELECT date, club, country, elo FROM raw_eloRatings")

    df_matches, df_elo = clean(df_matches, df_elo)

    # ============================================================
    # STEP 4-9: Dimensions
    # ============================================================
    dimension_maps = load_dimensions(dw_cnx, dw_cur, df_matches, df_elo)

    # ============================================================
    # STEP 10: Fact table
    # ============================================================
    inserted = load_fact_matches(dw_cnx, dw_cur, df_matches, dimension_maps)

    # ============================================================
    # STEP 11: Export dimension tables to CSV
    # ============================================================
    export_dimension_tables(dw_cur, clean_csv_dir)

    # ============================================================
    # STEP 12: Summary
    # ============================================================
    print_summary(dw_cur)

    # Close connection
    dw_cur.close()
    dw_cnx.close()

    print('\nData warehouse loaded successfully!')
    print(f'Raw data saved to: {raw_csv_dir}')
    print(f'Dimension data saved to: {clean_csv_dir}')


if __name__ == '__main__':
    main()
