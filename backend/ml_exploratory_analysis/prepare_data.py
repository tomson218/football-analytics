"""
prepare_data.py — Load data from football_dw data warehouse for ML analysis.
Data comes from fact_matches table and dimensions dim_date, dim_division, dim_team.
Data in fact_matches is already cleaned by ETL (etl_raw_to_dw.py), so no cleaning needed.

Export: data/matches_cleaned.csv
"""
import mysql.connector
import pandas as pd
import os
import sys

# Add database/ directory to path to import db_config
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database'))
from db_config import get_db_config

# Path to data/ folder
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "data")
os.makedirs(data_dir, exist_ok=True)


def load_matches_from_dw() -> pd.DataFrame:
    """
    Loads data from v_matches_ml view in football_dw data warehouse.
    The view contains a subset of columns needed for the ML model (HomeNoLose):
    Division, HomeTeam, AwayTeam, HomeElo, AwayElo, Form3Home, Form5Home,
    Form3Away, Form5Away, FTResult, OddHome, OddDraw, OddAway, MaxHome,
    MaxDraw, MaxAway, Over25, Under25, MaxOver25, MaxUnder25, HandiSize,
    HandiHome, HandiAway, C_LTH, C_LTA, C_VHD, C_VAD, C_HTB, C_PHB, MatchDate
    """
    dw_config = get_db_config()
    cnx = mysql.connector.connect(**dw_config)

    query = "SELECT * FROM v_matches_ml"

    df = pd.read_sql(query, cnx)
    cnx.close()

    return df


if __name__ == "__main__":
    print("Loading data from football_dw data warehouse...")
    df = load_matches_from_dw()
    print(f"Loaded {len(df)} matches.")
    print(f"Columns: {list(df.columns)}")
    print(f"\nResult distribution (FTResult):")
    print(df["FTResult"].value_counts())

    # Export to CSV
    csv_path = os.path.join(data_dir, "matches_cleaned.csv")
    df.to_csv(csv_path, index=False)
    print(f"\nData saved to {csv_path}")
