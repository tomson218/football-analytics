"""
load_dimensions.py — Main orchestrator for loading all 5 dimension tables.
"""
from common.constants import DIVISION_TO_COUNTRY, BATCH_SIZE, DAY_NAMES, MONTH_NAMES

from truncate_dw import truncate_dw_tables
from dim_country import load_dim_country
from dim_division import load_dim_division
from dim_team import load_dim_team
from dim_season import load_dim_season
from dim_date import load_dim_date


def load_dimensions(cnx, cursor, df_matches, df_elo):
    """Main function to load all dimensions."""
    # Truncate DW tables
    truncate_dw_tables(cnx, cursor)

    # dim_country
    country_id_cache = load_dim_country(cnx, cursor, df_elo, DIVISION_TO_COUNTRY)

    # Helper function with closed country_id_cache
    def get_or_create_country(country_code):
        if country_code in country_id_cache:
            return country_id_cache[country_code]
        cursor.execute("""
            INSERT INTO dim_country (country_code, name) VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE country_key = LAST_INSERT_ID(country_key)
        """, (country_code, country_code))
        country_key = cursor.lastrowid
        country_id_cache[country_key] = country_key
        return country_key

    # dim_division
    division_code_to_key = load_dim_division(cnx, cursor, df_matches, DIVISION_TO_COUNTRY, get_or_create_country)

    # dim_team
    team_id_cache = load_dim_team(cnx, cursor, df_elo, df_matches, DIVISION_TO_COUNTRY, get_or_create_country)

    # dim_season
    seasons, season_name_to_key, date_to_season = load_dim_season(cnx, cursor, df_matches)

    # dim_date
    date_to_key = load_dim_date(cnx, cursor, df_matches, date_to_season, BATCH_SIZE, DAY_NAMES, MONTH_NAMES)

    return {
        'country_id_cache': country_id_cache,
        'division_code_to_key': division_code_to_key,
        'team_id_cache': team_id_cache,
        'season_name_to_key': season_name_to_key,
        'date_to_season': date_to_season,
        'date_to_key': date_to_key,
    }
