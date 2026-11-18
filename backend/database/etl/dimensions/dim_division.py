"""
dim_division.py — Load dim_division.
"""


def load_dim_division(cnx, cursor, df_matches, division_to_country, get_or_create_country):
    """STEP 6: Load dim_division."""
    print('6. Loading dim_division...')

    unique_divisions = df_matches['Division'].dropna().unique()
    for div in unique_divisions:
        country_code = division_to_country.get(div, 'GER')
        country_key = get_or_create_country(country_code)
        cursor.execute("""
            INSERT INTO dim_division (division_code, name, country_key, country_code, country_name)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE division_key = LAST_INSERT_ID(division_key)
        """, (div, f'Division {div}', country_key, country_code, country_code))

    cnx.commit()
    print(f'   Loaded {len(unique_divisions)} divisions.')

    # Build map: division_code -> division_key
    division_code_to_key = {}
    cursor.execute("SELECT division_key, division_code FROM dim_division")
    for dk, dc in cursor.fetchall():
        division_code_to_key[dc] = dk
    return division_code_to_key
