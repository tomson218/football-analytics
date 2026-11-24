"""
prediction/data_stats.py — Query the data warehouse for dataset statistics.
Returns match count, league count, and season range.
"""
from mysql.connector import connect
from database.db_config import get_db_config


def get_data_stats():
    """
    Query fact_matches and dimension tables to return dynamic dataset stats:
    - total_matches: number of rows in fact_matches
    - total_leagues: number of distinct divisions
    - season_start: earliest season (e.g. '2020/21')
    - season_end: latest season (e.g. '2024/25')
    """
    with connect(**get_db_config()) as conn, conn.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT
                COUNT(*) AS total_matches,
                COUNT(DISTINCT d.division_code) AS total_leagues,
                MIN(dt.season_name) AS season_start,
                MAX(dt.season_name) AS season_end
            FROM fact_matches f
            JOIN dim_division d ON f.division_key = d.division_key
            JOIN dim_date dt ON f.date_key = dt.date_key
        """)
        return cursor.fetchone()
