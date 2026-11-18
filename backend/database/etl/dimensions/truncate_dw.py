"""
truncate_dw.py — Truncate old DW tables for restart.
"""


def truncate_dw_tables(cnx, cursor):
    """Truncate old DW tables (restart)."""
    print('4. Truncating old DW tables...')
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table in ['fact_matches', 'dim_team', 'dim_division', 'dim_country', 'dim_season', 'dim_date']:
        cursor.execute(f"TRUNCATE TABLE {table}")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    cnx.commit()
    print('   DW tables truncated.')
