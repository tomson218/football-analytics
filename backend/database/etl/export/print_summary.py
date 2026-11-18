"""
print_summary.py — Print data warehouse summary.
"""

SUMMARY_TABLES = [
    'dim_country', 'dim_division', 'dim_team', 'dim_season', 'dim_date',
    'fact_matches', 'raw_eloRatings', 'raw_Matches',
]


def print_summary(cursor):
    """STEP 12: Data warehouse summary."""
    print('\n=== DATA WAREHOUSE SUMMARY ===')
    for table in SUMMARY_TABLES:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"  {table + ':':<16}{cursor.fetchone()[0]} records")
