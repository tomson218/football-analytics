"""
dim_country.py — Load dim_country from raw_eloRatings + league mapping.
"""
import pandas as pd


def load_dim_country(cnx, cursor, df_elo, division_to_country):
    """STEP 5: Load dim_country from raw_eloRatings + league mapping."""
    print('5. Loading dim_country...')

    country_id_cache = {}
    def get_or_create_country(country_code):
        if country_code in country_id_cache:
            return country_id_cache[country_code]
        cursor.execute("""
            INSERT INTO dim_country (country_code, name) VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE country_key = LAST_INSERT_ID(country_key)
        """, (country_code, country_code))
        country_key = cursor.lastrowid
        country_id_cache[country_code] = country_key
        return country_key

    # Countries from Elo
    if 'country' in df_elo.columns:
        unique_countries = df_elo['country'].dropna().unique()
        for country in unique_countries:
            get_or_create_country(country)

    # Countries from league mapping
    for country_code in division_to_country.values():
        get_or_create_country(country_code)

    cnx.commit()
    print(f'   Loaded {len(country_id_cache)} countries.')
    return country_id_cache
