"""
load_raw_matches.py — Load Matches.csv → raw_Matches (DW) with filter.
"""
import pandas as pd
import os


def load_raw_matches(cnx, cursor, csv_dir, top_leagues, start_date, end_date, batch_size, raw_matches_columns):
    """Load Matches.csv → raw_Matches (DW) with filter: top leagues + dates."""
    print('   2b. Loading Matches.csv -> raw_Matches (DW)...')
    df_raw_matches = pd.read_csv(os.path.join(csv_dir, 'raw_Matches.csv'))
    df_raw_matches = df_raw_matches[
        df_raw_matches['Division'].isin(top_leagues) &
        df_raw_matches['MatchDate'].between(start_date, end_date)
    ]
    # Replace NaN with None for mysql.connector
    df_raw_matches = df_raw_matches.where(df_raw_matches.notna(), None)
    match_rows = df_raw_matches.values.tolist()

    col_names = ', '.join(raw_matches_columns)
    placeholders = ', '.join(['%s'] * len(raw_matches_columns))

    inserted = 0
    for i in range(0, len(match_rows), batch_size):
        batch = match_rows[i:i + batch_size]
        for row in batch:
            cursor.execute(
                f"INSERT INTO raw_Matches ({col_names}) VALUES ({placeholders})",
                row
            )
        cnx.commit()
        inserted += len(batch)
        print(f'   Loaded {min(i + batch_size, len(match_rows))}/{len(match_rows)} matches to raw_Matches (DW).')

    print(f'   Total loaded {len(match_rows)} matches to raw_Matches (DW).')
    return len(match_rows)
