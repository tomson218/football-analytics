"""
load_raw_elo.py — Load eloRatings.csv → raw_eloRatings (DW).
"""
import pandas as pd
import os


def load_raw_elo(cnx, cursor, csv_dir, start_date, end_date, batch_size):
    """Load eloRatings.csv → raw_eloRatings (DW)."""
    print('   2a. Loading eloRatings.csv -> raw_eloRatings (DW)...')
    df_raw_elo = pd.read_csv(os.path.join(csv_dir, 'raw_eloRatings.csv'))
    df_raw_elo = df_raw_elo[pd.to_datetime(df_raw_elo['date']).between(start_date, end_date)]
    elo_rows = df_raw_elo.values.tolist()

    for i in range(0, len(elo_rows), batch_size):
        batch = elo_rows[i:i + batch_size]
        cursor.executemany(
            "INSERT INTO raw_eloRatings (date, club, country, elo) VALUES (%s, %s, %s, %s)",
            batch
        )
        cnx.commit()
    print(f'   Loaded {len(elo_rows)} Elo records to raw_eloRatings (DW).')
    return len(elo_rows)
