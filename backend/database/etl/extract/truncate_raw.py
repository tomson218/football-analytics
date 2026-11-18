"""
truncate_raw.py — Truncate raw tables in football_dw for restart.
"""


def truncate_raw_tables(cnx, cursor):
    """Truncate raw tables in football_dw (restart)."""
    print('1. Truncating raw tables in football_dw...')
    cursor.execute("TRUNCATE TABLE raw_eloRatings")
    cursor.execute("TRUNCATE TABLE raw_Matches")
    cnx.commit()
    print('   Raw tables truncated.')
