"""
dim_team.py — Load dim_team from raw_eloRatings + raw_Matches.
"""
import pandas as pd


def load_dim_team(cnx, cursor, df_elo, df_matches, division_to_country, get_or_create_country):
    """STEP 7: Load dim_team from raw_eloRatings + raw_Matches."""
    print('7. Loading dim_team...')

    team_id_cache = {}
    def get_or_create_team(team_name, country_code):
        key = (team_name, country_code)
        if key in team_id_cache:
            return team_id_cache[key]
        country_key = get_or_create_country(country_code)
        cursor.execute("""
            INSERT INTO dim_team (name, country_key, country_code, country_name, record_type, valid_from)
            VALUES (%s, %s, %s, %s, 'current', CURDATE())
            ON DUPLICATE KEY UPDATE team_key = LAST_INSERT_ID(team_key)
        """, (team_name, country_key, country_code, country_code))
        team_key = cursor.lastrowid
        team_id_cache[key] = team_key
        return team_key

    # Register teams from Elo
    if 'club' in df_elo.columns and 'country' in df_elo.columns:
        for _, row in df_elo.iterrows():
            if pd.notna(row['club']) and pd.notna(row['country']):
                get_or_create_team(row['club'], row['country'])

    # Register teams from matches
    for _, row in df_matches.iterrows():
        div = row['Division']
        country_code = division_to_country.get(div, 'GER')
        if pd.notna(row['HomeTeam']):
            get_or_create_team(row['HomeTeam'], country_code)
        if pd.notna(row['AwayTeam']):
            get_or_create_team(row['AwayTeam'], country_code)

    cnx.commit()

    # Get latest Elo for each team
    elo_map = {}
    if 'club' in df_elo.columns and 'country' in df_elo.columns:
        df_elo_sorted = df_elo.sort_values('date')
        last_elo = df_elo_sorted.drop_duplicates(subset=['club', 'country'], keep='last')
        for _, row in last_elo.iterrows():
            club_name = row['club']
            country_name = row['country']
            if pd.notna(club_name) and pd.notna(country_name) and pd.notna(row['elo']):
                key = (club_name, country_name)
                if key in team_id_cache:
                    elo_map[team_id_cache[key]] = float(row['elo'])

    # Update Elo in dim_team
    for team_key, elo_score in elo_map.items():
        cursor.execute("""
            UPDATE dim_team SET current_elo = %s WHERE team_key = %s
        """, (elo_score, team_key))
    cnx.commit()
    print(f'   Loaded {len(team_id_cache)} teams.')
    return team_id_cache
